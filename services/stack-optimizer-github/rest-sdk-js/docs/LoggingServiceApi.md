# ApssApi.LoggingServiceApi

All URIs are relative to *http://localhost/stack-optimizer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getAllLoggersUsingGET**](LoggingServiceApi.md#getAllLoggersUsingGET) | **GET** /logger/getAllLoggers | Get All Logging level
[**updateLogLevelUsingPOST**](LoggingServiceApi.md#updateLogLevelUsingPOST) | **POST** /logger/{loggerName}/{logLevel} | Update the Logging level



## getAllLoggersUsingGET

> Object getAllLoggersUsingGET(opts)

Get All Logging level

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.LoggingServiceApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.getAllLoggersUsingGET(opts).then((data) => {
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
- **Accept**: application/json


## updateLogLevelUsingPOST

> Object updateLogLevelUsingPOST(loggerName, logLevel, opts)

Update the Logging level

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.LoggingServiceApi();
let loggerName = "loggerName_example"; // String | loggerName
let logLevel = "logLevel_example"; // String | logLevel
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.updateLogLevelUsingPOST(loggerName, logLevel, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **loggerName** | **String**| loggerName | 
 **logLevel** | **String**| logLevel | 
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

**Object**

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

