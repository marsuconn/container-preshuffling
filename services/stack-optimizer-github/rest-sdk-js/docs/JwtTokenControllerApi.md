# ApssApi.JwtTokenControllerApi

All URIs are relative to *http://localhost/stack-optimizer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**jwtSampleUsingDELETE**](JwtTokenControllerApi.md#jwtSampleUsingDELETE) | **DELETE** /sample | jwtSample
[**jwtSampleUsingGET**](JwtTokenControllerApi.md#jwtSampleUsingGET) | **GET** /sample | jwtSample
[**jwtSampleUsingHEAD**](JwtTokenControllerApi.md#jwtSampleUsingHEAD) | **HEAD** /sample | jwtSample
[**jwtSampleUsingOPTIONS**](JwtTokenControllerApi.md#jwtSampleUsingOPTIONS) | **OPTIONS** /sample | jwtSample
[**jwtSampleUsingPATCH**](JwtTokenControllerApi.md#jwtSampleUsingPATCH) | **PATCH** /sample | jwtSample
[**jwtSampleUsingPOST**](JwtTokenControllerApi.md#jwtSampleUsingPOST) | **POST** /sample | jwtSample
[**jwtSampleUsingPUT**](JwtTokenControllerApi.md#jwtSampleUsingPUT) | **PUT** /sample | jwtSample



## jwtSampleUsingDELETE

> Object jwtSampleUsingDELETE(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingDELETE(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## jwtSampleUsingGET

> Object jwtSampleUsingGET(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingGET(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## jwtSampleUsingHEAD

> Object jwtSampleUsingHEAD(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingHEAD(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## jwtSampleUsingOPTIONS

> Object jwtSampleUsingOPTIONS(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingOPTIONS(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## jwtSampleUsingPATCH

> Object jwtSampleUsingPATCH(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingPATCH(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## jwtSampleUsingPOST

> Object jwtSampleUsingPOST(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingPOST(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## jwtSampleUsingPUT

> Object jwtSampleUsingPUT(opts)

jwtSample

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.JwtTokenControllerApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.jwtSampleUsingPUT(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*

