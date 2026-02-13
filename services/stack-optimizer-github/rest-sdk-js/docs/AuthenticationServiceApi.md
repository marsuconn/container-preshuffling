# ApssApi.AuthenticationServiceApi

All URIs are relative to *http://localhost/stack-optimizer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authenticateUsingPOST**](AuthenticationServiceApi.md#authenticateUsingPOST) | **POST** /dev/authenticate | authenticate



## authenticateUsingPOST

> authenticateUsingPOST(opts)

authenticate

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.AuthenticationServiceApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'", // String | 
  'password': "password_example", // String | password
  'username': "username_example" // String | username
};
apiInstance.authenticateUsingPOST(opts).then(() => {
  console.log('API called successfully.');
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]
 **password** | **String**| password | [optional] 
 **username** | **String**| username | [optional] 

### Return type

null (empty response body)

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

