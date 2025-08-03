@@ .. @@
     # Check required fields
-    for field in VALIDATION_RULES['required_fields']:
+    required_fields = ['nom']  # Only nom is required now
+    for field in required_fields:
         if not data.get(field, '').strip():
             return {
                 'valid': False, 
                 'message': f"{field.capitalize()} est requis!"
             }