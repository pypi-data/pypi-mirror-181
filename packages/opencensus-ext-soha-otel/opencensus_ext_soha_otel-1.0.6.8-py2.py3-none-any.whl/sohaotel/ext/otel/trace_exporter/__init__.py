# Copyright 2022, SohaTv Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Export the spans data to Cyber Trace."""
import datetime
import json
import logging

import backoff
import requests
from time import sleep

from opencensus.common.transports import sync
from opencensus.trace import base_exporter

__version__ = "1.0.6.8"

DEFAULT_ENDPOINT = 'https://cybertrace.sohatv.vn/v1/traces'
SOHA_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Soha Otel OTLP Exporter Python2/" + __version__,
}

# Work around API change between backoff 1.x and 2.x. Since 2.0.0 the backoff
# wait generator API requires a first .send(None) before reading the backoff
# values from the generator.
_is_backoff_v2 = next(backoff.expo()) is None


def _expo(*args, **kwargs):
    gen = backoff.expo(*args, **kwargs)
    if _is_backoff_v2:
        gen.send(None)
    return gen


SOHA_ISO_DATETIME_REGEX = '%Y-%m-%dT%H:%M:%S.%fZ'

SUCCESS_STATUS_CODE = (200, 202)


class SohaOtelHttpExporter(base_exporter.Exporter):
    def __init__(
            self,
            service_name='my_service',
            endpoint=DEFAULT_ENDPOINT,
            transport=sync.SyncTransport,
            session=None,
            headers=None,
            timeout=None,
            skip_method=None,
            retry_able=False
    ):
        self.service_name = service_name
        self.endpoint = endpoint
        self._session = session or requests.Session()
        self.transport = transport(self)
        self._headers = headers or SOHA_HEADERS
        self._session.headers.update(self._headers)
        self.retry_able = retry_able
        self._timeout = timeout
        self._shutdown = False
        self._MAX_RETRY_TIMEOUT = 64
        self.skip_method = skip_method

    @property
    def get_url(self):
        return self.endpoint

    @staticmethod
    def _retryable(resp):
        if resp.status_code == 408:
            return True
        if 500 <= resp.status_code <= 599:
            return True
        return False

    def _send_exporter(self, json_data):
        result = self._session.post(
            url=self.get_url,
            data=json_data,
            headers=self._headers,
            timeout=self._timeout,
        )

        if not self._retryable(result):
            logging.info("Success to send spans to CyberTrace. {status_code}".format(status_code=result.status_code))
            return True
        else:
            logging.error(
                "Failed to send spans to Cyber Trace server! Spans are {data}. Status: {status_code}".format(
                    data=json_data, status_code=result.status_code))
            return False

    def emit(self, span_datas):
        # emit span
        if self._shutdown:
            logging.warning("Exporter already shutdown, ignoring batch")
            return
        try:
            serialized_data = self.translate_to_soha_otel(span_datas)
            json_data = json.dumps(serialized_data)

            # not retry
            if not self.retry_able:
                self._send_exporter(json_data=json_data)
                return
            else:
                # retry able
                for delay in _expo(max_value=self._MAX_RETRY_TIMEOUT):
                    if delay == self._MAX_RETRY_TIMEOUT:
                        logging.error(
                            "Failed to send spans to Cyber Trace server! Spans are {}. Max retry time out!"
                            .format(json_data))
                        return
                    result = self._send_exporter(json_data=json_data)
                    if not result:
                        logging.info('delay: {delay}'.format(delay=delay))
                        sleep(delay)
                        continue
                    else:
                        break
        except Exception as e:  # pragma: NO COVER
            logging.error(getattr(e, 'message', e))

    def export(self, span_datas):
        self.transport.export(span_datas)

    def translate_to_soha_otel(self, span_datas):
        # convert data object from opencensus to soha-otel
        span_array = []
        for span in span_datas:
            start_timestamp_mus = time_to_timestamp(span.start_time)
            end_timestamp_mus = time_to_timestamp(span.end_time)
            link_array = _encode_links(span.links)
            attr_array = _extract_attr_from_span(span.attributes)
            events_array = _encode_events(span.message_events)

            # count
            dropped_attributes_count = 0 if attr_array is None or not isinstance(attr_array, list) else len(attr_array)
            dropped_link_count = 0 if link_array is None or not isinstance(link_array, list) else len(link_array)
            dropped_events_count = 0 if events_array is None or not isinstance(events_array, list) else len(events_array)

            # store code
            status_code = 1
            if span.status.code == 1:
                status_code = "STATUS_CODE_OK"
            elif span.status.code == 2:
                status_code = "STATUS_CODE_ERROR"
            item = {
                "traceId": span.context.trace_id,
                "spanId": str(span.span_id),
                "name": span.name,
                "kind": span.span_kind,
                "startTimeUnixNano": start_timestamp_mus,
                "endTimeUnixNano": end_timestamp_mus,
                "attributes": attr_array,
                "droppedAttributesCount": dropped_attributes_count,
                "events": events_array,
                "droppedEventsCount": dropped_events_count,
                "status": {
                    "code": span.status.code,
                    "message": span.status.message
                },
                "links": link_array,
                "droppedLinksCount": dropped_link_count
            }
            parent_span_id = span.parent_span_id
            span_kind = span.span_kind

            if span_kind is not None:
                item['kind'] = span_kind

            if parent_span_id is not None:
                item['parentSpanId'] = str(parent_span_id)

            span_array.append(item)

        return {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": _default_attr_lib(service_name=self.service_name),
                        "droppedAttributesCount": 0
                    },
                    "scopeSpans": [
                        {
                            "scope": {
                                "name": self.service_name,
                                "version": __version__
                            },
                            "spans": span_array
                        }
                    ]
                }
            ]
        }


def _default_attr_lib(service_name):
    return [
        {
            "key": "service.name",
            "value": {
                "stringValue": service_name
            }
        },
        {
            "key": "telemetry.sdk.language",
            "value": {
                "stringValue": 'py2'
            }
        },
        {
            "key": "telemetry.sdk.name",
            "value": {
                "stringValue": "opentelemetry"
            }
        },
        {
            "key": "telemetry.sdk.version",
            "value": {
                "stringValue": __version__
            }
        }
    ]


def _encode_links(links):
    attrs = []
    if links is None:
        return []

    try:
        for e in links:
            encoded_link = {
                "trace_id": e.context.trace_id,
                "span_id": e.context.span_id,
            }
            for key, value in e.attributes.items():
                try:
                    encoded_link["attributes"].append(
                        _encode_key_value(key, value)
                    )
                    # pylint: disable=broad-except
                except Exception as error:
                    logging.exception(error)
            attrs.append(encoded_link)
    except Exception as e:
        logging.error(getattr(e, 'message', e))

    return attrs


def _encode_key_value(attribute_key, attribute_value):
    if isinstance(attribute_value, int):
        return {
            'key': attribute_key,
            'value': {
                'intValue': attribute_value
            }
        }

    if isinstance(attribute_value, float):
        return {
            'key': attribute_key,
            'value': {
                'doubleValue': attribute_value
            }
        }

    if isinstance(attribute_value, bool):
        return {
            'key': attribute_key,
            'value': {
                'boolValue': attribute_value
            }
        }
    elif isinstance(attribute_value, str):
        return {
            'key': attribute_key,
            'value': {
                'stringValue': attribute_value
            }
        }
    else:
        logging.warning('Could not serialize attr %s', attribute_key)


def _extract_attr_from_span(attr):
    attrs = []
    try:
        if attr is None:
            return attrs
        for attribute_key, attribute_value in attr.items():
            attrs.append(_encode_key_value(attribute_key=attribute_key, attribute_value=attribute_value))
    except Exception as e:
        logging.error(getattr(e, 'message', e))
    return attrs


def _encode_events(events):
    result = []
    try:
        if events is None:
            return []

        for item in events:
            encoded_event = {
                'name': item.description,
                'time_unix_nano': time_to_timestamp(item.timestamp),
            }
            events.append(encoded_event)
    except Exception as e:
        logging.error(getattr(e, 'message', e))

    return result


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def time_to_timestamp(timestamp):
    timestamp_str = datetime.datetime.strptime(timestamp, SOHA_ISO_DATETIME_REGEX)
    rs = int(unix_time_millis(timestamp_str)) * 1000000
    return rs
