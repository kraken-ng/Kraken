# Bugs

**Pending to fix:**

- In the command "grep" the wildcards do not work in Windows.
- In the command "find" the wildcards do not work on Windows.
- In the command "chmod" (PHP + Windows), when executed, it does not return any error but does not make any change (maybe it is because of the octal).
- In the command "grep" of PHP in Windows/Linux, fix the logic so that it continues searching even if it finds errors (exceptions issue).
- In the Java Upload module, when the chunk data size is greater than 62418 bytes nothing is received in the "data" parameter. It may have something to do with the maximum of 65Kb per page in JSP).
- In the Java Upload module for Windows, sometimes an unexpected error is returned: "<UPLOAD_FILE_PATH> (The process does not have access to the file because it is being used by another process)". To solve it, simply continue from the last seek and increase delay between requests.
