# ApssApi.UserDetailsServiceApi

All URIs are relative to *http://localhost/stack-optimizer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getUserDetailsUsingPOST**](UserDetailsServiceApi.md#getUserDetailsUsingPOST) | **POST** /getUserDetails | getUserDetails
[**verifyUserDetailsUsingPOST**](UserDetailsServiceApi.md#verifyUserDetailsUsingPOST) | **POST** /verifyUserDetails | verifyUserDetails



## getUserDetailsUsingPOST

> UserBean getUserDetailsUsingPOST(opts)

getUserDetails

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.UserDetailsServiceApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.getUserDetailsUsingPOST(opts).then((data) => {
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

[**UserBean**](UserBean.md)

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## verifyUserDetailsUsingPOST

> UserBean verifyUserDetailsUsingPOST(opts)

verifyUserDetails

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.UserDetailsServiceApi();
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.verifyUserDetailsUsingPOST(opts).then((data) => {
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

[**UserBean**](UserBean.md)

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*

