//use LOCAL_BG_SEC;
db.createCollection("BG_SECURITY_WHITELISTED_URLS");
db.createCollection("BG_SECURITY_API_PERMISSIONS");
db.createCollection("BG_SECURITY_DISABLED_URLS");
db.BG_SECURITY_WHITELISTED_URLS.insert({
                                        "_id" : ObjectId("61e53e83213c6d6e9cff60a9"),
                                        "servletPaths" : [
                                            "/csrf",
                                            "/v2/api-docs",
                                            "/swagger-resources",
                                            "/configuration/ui",
                                            "/configuration/security",
                                            "/swagger-ui.html",
                                            "/webjars/",
                                            "/v3/api-docs/",
                                            "/swagger-ui/",
                                            "/blumeSecurity/refresh"
                                        ]
                                    });
db.BG_SECURITY_API_PERMISSIONS.insert({ "permissions" : [
                                              "Blume Collaboration Center"
                                          ],
                                          "conditionType" : "AND",
                                          "apiSignature" : {
                                              "servletPath" : "/sayHello",
                                              "methods" : [
                                                  "GET",
                                                  "POST",
                                                  "PUT",
                                                  "DELETE"
                                              ]
                                          },
                                          "contextPath" : "/"
                                      })

db.BG_SECURITY_API_PERMISSIONS.insert({
                                          "permissions" : [
                                              "Blume Collaboration Center"
                                          ],
                                          "conditionType" : "AND",
                                          "apiSignature" : {
                                              "methods" : [
                                                  "GET",
                                                  "POST",
                                                  "PUT",
                                                  "DELETE"
                                              ]
                                          },
                                          "contextPath" : "/"
                                      })