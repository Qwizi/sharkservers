"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.request = exports.catchErrorCodes = exports.getResponseBody = exports.getResponseHeader = exports.sendRequest = exports.getRequestBody = exports.getHeaders = exports.resolve = exports.getFormData = exports.getQueryString = exports.base64 = exports.isSuccess = exports.isFormData = exports.isBlob = exports.isStringWithValue = exports.isString = exports.isDefined = void 0;
/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
const axios_1 = __importDefault(require("axios"));
const form_data_1 = __importDefault(require("form-data"));
const ApiError_1 = require("./ApiError");
const CancelablePromise_1 = require("./CancelablePromise");
const isDefined = (value) => {
    return value !== undefined && value !== null;
};
exports.isDefined = isDefined;
const isString = (value) => {
    return typeof value === 'string';
};
exports.isString = isString;
const isStringWithValue = (value) => {
    return (0, exports.isString)(value) && value !== '';
};
exports.isStringWithValue = isStringWithValue;
const isBlob = (value) => {
    return (typeof value === 'object' &&
        typeof value.type === 'string' &&
        typeof value.stream === 'function' &&
        typeof value.arrayBuffer === 'function' &&
        typeof value.constructor === 'function' &&
        typeof value.constructor.name === 'string' &&
        /^(Blob|File)$/.test(value.constructor.name) &&
        /^(Blob|File)$/.test(value[Symbol.toStringTag]));
};
exports.isBlob = isBlob;
const isFormData = (value) => {
    return value instanceof form_data_1.default;
};
exports.isFormData = isFormData;
const isSuccess = (status) => {
    return status >= 200 && status < 300;
};
exports.isSuccess = isSuccess;
const base64 = (str) => {
    try {
        return btoa(str);
    }
    catch (err) {
        // @ts-ignore
        return Buffer.from(str).toString('base64');
    }
};
exports.base64 = base64;
const getQueryString = (params) => {
    const qs = [];
    const append = (key, value) => {
        qs.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`);
    };
    const process = (key, value) => {
        if ((0, exports.isDefined)(value)) {
            if (Array.isArray(value)) {
                value.forEach(v => {
                    process(key, v);
                });
            }
            else if (typeof value === 'object') {
                Object.entries(value).forEach(([k, v]) => {
                    process(`${key}[${k}]`, v);
                });
            }
            else {
                append(key, value);
            }
        }
    };
    Object.entries(params).forEach(([key, value]) => {
        process(key, value);
    });
    if (qs.length > 0) {
        return `?${qs.join('&')}`;
    }
    return '';
};
exports.getQueryString = getQueryString;
const getUrl = (config, options) => {
    const encoder = config.ENCODE_PATH || encodeURI;
    const path = options.url
        .replace('{api-version}', config.VERSION)
        .replace(/{(.*?)}/g, (substring, group) => {
        if (options.path?.hasOwnProperty(group)) {
            return encoder(String(options.path[group]));
        }
        return substring;
    });
    const url = `${config.BASE}${path}`;
    if (options.query) {
        return `${url}${(0, exports.getQueryString)(options.query)}`;
    }
    return url;
};
const getFormData = (options) => {
    if (options.formData) {
        const formData = new form_data_1.default();
        const process = (key, value) => {
            if ((0, exports.isString)(value) || (0, exports.isBlob)(value)) {
                formData.append(key, value);
            }
            else {
                formData.append(key, JSON.stringify(value));
            }
        };
        Object.entries(options.formData)
            .filter(([_, value]) => (0, exports.isDefined)(value))
            .forEach(([key, value]) => {
            if (Array.isArray(value)) {
                value.forEach(v => process(key, v));
            }
            else {
                process(key, value);
            }
        });
        return formData;
    }
    return undefined;
};
exports.getFormData = getFormData;
const resolve = async (options, resolver) => {
    if (typeof resolver === 'function') {
        return resolver(options);
    }
    return resolver;
};
exports.resolve = resolve;
const getHeaders = async (config, options, formData) => {
    const token = await (0, exports.resolve)(options, config.TOKEN);
    const username = await (0, exports.resolve)(options, config.USERNAME);
    const password = await (0, exports.resolve)(options, config.PASSWORD);
    const additionalHeaders = await (0, exports.resolve)(options, config.HEADERS);
    const formHeaders = typeof formData?.getHeaders === 'function' && formData?.getHeaders() || {};
    const headers = Object.entries({
        Accept: 'application/json',
        ...additionalHeaders,
        ...options.headers,
        ...formHeaders,
    })
        .filter(([_, value]) => (0, exports.isDefined)(value))
        .reduce((headers, [key, value]) => ({
        ...headers,
        [key]: String(value),
    }), {});
    if ((0, exports.isStringWithValue)(token)) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    if ((0, exports.isStringWithValue)(username) && (0, exports.isStringWithValue)(password)) {
        const credentials = (0, exports.base64)(`${username}:${password}`);
        headers['Authorization'] = `Basic ${credentials}`;
    }
    if (options.body) {
        if (options.mediaType) {
            headers['Content-Type'] = options.mediaType;
        }
        else if ((0, exports.isBlob)(options.body)) {
            headers['Content-Type'] = options.body.type || 'application/octet-stream';
        }
        else if ((0, exports.isString)(options.body)) {
            headers['Content-Type'] = 'text/plain';
        }
        else if (!(0, exports.isFormData)(options.body)) {
            headers['Content-Type'] = 'application/json';
        }
    }
    return headers;
};
exports.getHeaders = getHeaders;
const getRequestBody = (options) => {
    if (options.body) {
        return options.body;
    }
    return undefined;
};
exports.getRequestBody = getRequestBody;
const sendRequest = async (config, options, url, body, formData, headers, onCancel, axiosClient) => {
    const source = axios_1.default.CancelToken.source();
    const requestConfig = {
        url,
        headers,
        data: body ?? formData,
        method: options.method,
        withCredentials: config.WITH_CREDENTIALS,
        cancelToken: source.token,
    };
    onCancel(() => source.cancel('The user aborted a request.'));
    try {
        return await axiosClient.request(requestConfig);
    }
    catch (error) {
        const axiosError = error;
        if (axiosError.response) {
            return axiosError.response;
        }
        throw error;
    }
};
exports.sendRequest = sendRequest;
const getResponseHeader = (response, responseHeader) => {
    if (responseHeader) {
        const content = response.headers[responseHeader];
        if ((0, exports.isString)(content)) {
            return content;
        }
    }
    return undefined;
};
exports.getResponseHeader = getResponseHeader;
const getResponseBody = (response) => {
    if (response.status !== 204) {
        return response.data;
    }
    return undefined;
};
exports.getResponseBody = getResponseBody;
const catchErrorCodes = (options, result) => {
    const errors = {
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        ...options.errors,
    };
    const error = errors[result.status];
    if (error) {
        throw new ApiError_1.ApiError(options, result, error);
    }
    if (!result.ok) {
        const errorStatus = result.status ?? 'unknown';
        const errorStatusText = result.statusText ?? 'unknown';
        const errorBody = (() => {
            try {
                return JSON.stringify(result.body, null, 2);
            }
            catch (e) {
                return undefined;
            }
        })();
        throw new ApiError_1.ApiError(options, result, `Generic Error: status: ${errorStatus}; status text: ${errorStatusText}; body: ${errorBody}`);
    }
};
exports.catchErrorCodes = catchErrorCodes;
/**
 * Request method
 * @param config The OpenAPI configuration object
 * @param options The request options from the service
 * @param axiosClient The axios client instance to use
 * @returns CancelablePromise<T>
 * @throws ApiError
 */
const request = (config, options, axiosClient = axios_1.default) => {
    return new CancelablePromise_1.CancelablePromise(async (resolve, reject, onCancel) => {
        try {
            const url = getUrl(config, options);
            const formData = (0, exports.getFormData)(options);
            const body = (0, exports.getRequestBody)(options);
            const headers = await (0, exports.getHeaders)(config, options, formData);
            if (!onCancel.isCancelled) {
                const response = await (0, exports.sendRequest)(config, options, url, body, formData, headers, onCancel, axiosClient);
                const responseBody = (0, exports.getResponseBody)(response);
                const responseHeader = (0, exports.getResponseHeader)(response, options.responseHeader);
                const result = {
                    url,
                    ok: (0, exports.isSuccess)(response.status),
                    status: response.status,
                    statusText: response.statusText,
                    body: responseHeader ?? responseBody,
                };
                (0, exports.catchErrorCodes)(options, result);
                resolve(result.body);
            }
        }
        catch (error) {
            reject(error);
        }
    });
};
exports.request = request;
