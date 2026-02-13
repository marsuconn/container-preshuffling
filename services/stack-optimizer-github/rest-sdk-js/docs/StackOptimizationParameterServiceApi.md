# ApssApi.StackOptimizationParameterServiceApi

All URIs are relative to *http://localhost/stack-optimizer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**deleteOptimizationParametersUsingDELETE**](StackOptimizationParameterServiceApi.md#deleteOptimizationParametersUsingDELETE) | **DELETE** /stackOptimizationParameter/{id} | deleteOptimizationParameters
[**getOptimizationParametersByLocationIdUsingGET**](StackOptimizationParameterServiceApi.md#getOptimizationParametersByLocationIdUsingGET) | **GET** /stackOptimizationParameter | getOptimizationParametersByLocationId
[**saveStackOptimizationParametersUsingPOST**](StackOptimizationParameterServiceApi.md#saveStackOptimizationParametersUsingPOST) | **POST** /stackOptimizationParameter | saveStackOptimizationParameters



## deleteOptimizationParametersUsingDELETE

> ApiResponse deleteOptimizationParametersUsingDELETE(id, opts)

deleteOptimizationParameters

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.StackOptimizationParameterServiceApi();
let id = 789; // Number | id
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.deleteOptimizationParametersUsingDELETE(id, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| id | 
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

[**ApiResponse**](ApiResponse.md)

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## getOptimizationParametersByLocationIdUsingGET

> ApiResponseOfListOfOptimizationParametersDTO getOptimizationParametersByLocationIdUsingGET(locationUUID, opts)

getOptimizationParametersByLocationId

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.StackOptimizationParameterServiceApi();
let locationUUID = "locationUUID_example"; // String | locationUUID
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.getOptimizationParametersByLocationIdUsingGET(locationUUID, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **locationUUID** | **String**| locationUUID | 
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

[**ApiResponseOfListOfOptimizationParametersDTO**](ApiResponseOfListOfOptimizationParametersDTO.md)

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## saveStackOptimizationParametersUsingPOST

> ApiResponseOfOptimizationParametersSavedDTO saveStackOptimizationParametersUsingPOST(optimizationParametersDTO, opts)

saveStackOptimizationParameters

### Example

```javascript
import ApssApi from 'apss_api';
let defaultClient = ApssApi.ApiClient.instance;
// Configure API key authorization: JWT
let JWT = defaultClient.authentications['JWT'];
JWT.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//JWT.apiKeyPrefix = 'Token';

let apiInstance = new ApssApi.StackOptimizationParameterServiceApi();
let optimizationParametersDTO = new ApssApi.OptimizationParametersDTO(); // OptimizationParametersDTO | optimizationParametersDTO
let opts = {
  'authorization': "'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A'" // String | 
};
apiInstance.saveStackOptimizationParametersUsingPOST(optimizationParametersDTO, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **optimizationParametersDTO** | [**OptimizationParametersDTO**](OptimizationParametersDTO.md)| optimizationParametersDTO | 
 **authorization** | **String**|  | [optional] [default to &#39;eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJvcmdhbml6YXRpb25UeXBlIjoiQWRtaW4iLCJvcmdhbml6YXRpb25UeXBlcyI6WyJBZG1pbiJdLCJzdWIiOiJiaXpUb0JpekBibHVtZS5jb20iLCJmaXJzdE5hbWUiOiJCaXoiLCJsYXN0TmFtZSI6IkJpeiIsImVtYWlsQWRkcmVzcyI6ImJpelRvQml6QGJsdW1lLmNvbSIsIm9yZ2FuaXphdGlvblV1aWQiOiI3NWRhZjIyNi05NWQ3LTQwZDgtYTk0NC03YWUyYTI1MDg1ZDYiLCJwaG9uZU51bWJlciI6Ijc4MS14eHgteXl5eSIsIm9yZ2FuaXphdGlvbk5hbWUiOiJSRVotMSIsIm9yZ2FuaXphdGlvbkNvZGUiOiJSRVoxXzcyIiwib3JnYW5pemF0aW9uRGJJZCI6MCwiYnVzaW5lc3NBZGRyZXNzIjoiIn0.WEkoKJb5wzzmwGK3eRa1y3QnRKozfbC_BP3kIyDlGPL3ZAdYWF9Akagbc6SJZptrV_TSiGQE4BajNyz1LLs38A&#39;]

### Return type

[**ApiResponseOfOptimizationParametersSavedDTO**](ApiResponseOfOptimizationParametersSavedDTO.md)

### Authorization

[JWT](../README.md#JWT)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

