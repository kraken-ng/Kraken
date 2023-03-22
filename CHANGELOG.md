# Change Log

## [v1.1.0] - 2023-03-22

- Multiple bugs fixed:
  - "cp" (Java)
    - A missing try catch block has been added to control possible exceptions thrown during path normalization.
  - "dup_token" (NET)
    - The handle to the target process has been changed by using the OpenProcess function (which gives more control and allows specifying a flag to interact with PPL processes). Thanks to [Pablo Martinez](https://twitter.com/xassiz) for the notice and support.
    - We have also eliminated a block for checking the identity of the Current Thread that, on certain occasions, produced an unexpected error.
  - "execute" (JAVA)
    - A missing try catch block has been added to control possible exceptions thrown during path normalization.
  - "execute_with_token" (NET)
    - The CreateProcessWithToken function has been changed to CreateProcessAsUser. In previous versions, this module did not work correctly when using tokens from non-NT Authority System users. Thanks to the fix added by [Kurosh](https://twitter.com/_Kudaes_) in Hanshell I was able to port it to Kraken.
    - The same identity check block in the "dup_token" module has also been removed.
  - "reg_dump_trans" (NET), previously as secretsdump. (cc: @xassiz)
    - The name has been changed because the functionality that this module performed could be extended and, therefore, its functionality changed.
    - Extraction of any registry key is now supported.
    - Some missing functionalities have been added for the closing of the elements used by the module (transacted file rollback, closing of handlers and mapped view file).
    - The check based on administrative permissions has been changed to one based on SeBackup privilege. Since not all registry key extractions require administrative privileges, however, SeBackup is needed.
  - Fixed a bug in the standard Java agent that prevented correct operation in certain environments (Liferay).
  - Fixed a bug in the processing of the HTTP response returned by the agent.
- New modules:
  - "hotfixes": module to show hotfixes installed on current computer (via WMI). Thanks to [Etnum](https://twitter.com/the_etnum)
- New environments:
  - Different versions of Liferay environments have been added where the correct operation of Kraken Java agents has been validated..

## [v1.0.1] - 2023-03-13

- Added Kraken Wiki (with detailed information about the installation process and usage, as well as contributions in Kraken modules).
- New modules:
  - "mv": module to move files or directories.
- Mutiple bugs fixed:
  - Fixed some path normalization issues in all Java modules as well as in the template. 

## [v1.0.0] - 2023-02-25

- Multiple bugs fixed:
  - Adapted Kraken's modules to work in "1.6 >= Java <= 17" versions.
  - Fixed some path normalization issues in all PHP modules as well as in the template.
- New core features:
  - The "references" parameter has been added to the Kraken message passing structure. This parameter, which only works in NET, allows the specific references of each module to be added in the compilation process (csc). This avoids referencing unnecessary DLLs during this process. It also avoids a compilation error when there is no DLL in the system, as well as it allows the possibility of "linking" DLLs that the operator uploads directly to the target machine.
- New modules:
  - "sc": module to control services in NET implants using Service Controller functions.
- Updates in modules:
  - Java support has been added to the "id" module.
  - The "powerpick" module has been refactored and some existing bugs have been fixed.
  - PHP support has been added to the "tcpconnect" module.

## [v0.5.0] - 2023-02-13

- Multiple bugs fixed:
  - Fix bug in Java ls module that did not list the "." and ".." files.
  - Fix bug in Java ls module that did not correctly list a single file (because it was passed the relative path and not the absolute path)
  - Fix bug in Java rm module that it did not delete files properly and, for directories, did not control exceptions.
  - Fixed all the PHP, Java and .NET modules that were using Paths and were not sanitizing properly.
  - Fixed bug in Java ls module when using the recursive mode (the error was that the recursion went into the directories "." and "..").
  - Fixed bug in NET impersonate module when a password with special characters was not received correctly (a new dispatcher has been created)
  - Fixed bug in NET cat module because some refactoring issues
  - Fixed bug in all NET modules (even agent) when impersonate and access to special folders like "Documents" of any User Directory (Thanks @Balhissay to help me fix it!)
  - Fixed bug in most of PHP modules (Kraken only support php >=5.4) because there are some core functions that are not available in lower versions.
  - Fixed bug in Kraken's main when profile file not exists.
  - Adapted Kraken's modules to work in NET 3.5 version.
- Kraken redesign to extend and scale its operation:
  - The logic of the clients (c2 and standard) has been separated to independent files. This way, as each one has a different operation, they are not mixed and the code is much cleaner.
  - A "compilers" folder has been created, these files are used to define how the modules are treated depending on the agent used (php -> raw, java -> compile, etc).
  - The file containing all the dispatchers (for the modules) has been refactored and moved to separate files. In the same way as with the clients and compilers, the code is cleaner and more isolated from each other (it also avoids that, to add or touch a dispatcher, you have to affect all of them).
  - The "formaters" have been created, which are pieces of code to manage how the outputs of the modules are "treated" (for example, when they have columns, it is not enough to print them).
  - A "commands" file has been created to manage everything related to the commands, i.e. how the modules are treated, the loading depending on the agent context, search, etc.
  - The list of modules (which was included in the configuration) has been moved to a separate file located in the "modules" directory. This file will be the one that can be edited to register new commands/modules.
  - A "mods" file has been added for the management of modules used by the C2 client. Before it was a bit of a mess, because everything was done from the same client. I have simply separated it and I think it is now better structured.
  - A "printer" file has been created and is used to print in different colors.
  - The Selector has been created, which is the component in charge of communicating the actions received by the client with the agent. To do this, it chooses the dispatcher that corresponds to the command and passes the data bidirectionally.
  - A Token class has been created for the management of Tokens in .NET agents (it is simply cleaner and more organized).
  - Finally, it has cleaned up all the files, imports, function structure and other things that allow me to sleep more peacefully at night.
- New core features:
  - Core command "recompile" to recompile modules when using the "container" compiler (e.g. in Java agents).
  - Now, SIGINT (Ctrl-c) is detected in prompt and is managed in the right way.
- New modules:
  - "pspy": module to monitor running process on machine (idea from [pspy](https://github.com/DominicBreuker/pspy)).
  - "webinfo": module to get information from web server context (env vars, extensions, configuration values, components, etc).

## [v0.4.0] - 2022-12-14

- Multiple bugs fixed:
  - Fix bug for self-signed certificates or TLS errors.
  - Fix bug in NET download module due to permissions error on file reading.
  - Fix bug in CORE help command when passing a space instead of module.
  - Fix bug in NET ls module removing the ".\" when listing files.
  - Fix bug in formatting columns for some commands. [Columnar](https://pypi.org/project/columnar/) is now used to properly format columns in command output.
  - Fix bug in shell tabulation. The WordCompleter has been replaced by [NestedCompleter](https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html?highlight=NestedCompleter#prompt_toolkit.completion.NestedCompleter) which allows to nest completes (to tabulate by levels and show arguments) as well as to fix the existing bug.
  - Fix bug in agent communication. Now it is no longer forced to use only POST and FIELD.
  - Fix bug in the installation process when not installing correctly the python libraries. The installation method with conda/miniconda has been added and it works perfectly (both python version and libraries).
  - Fixed bug in Docker python library. The necessary configuration has been added to the installation so that the user is added to the docker group and the bug does not happen again.
  - Fixed bug in Docker when can not pull the image to use. Added a controlled exception.
  - *Partial* solution to the bug of paths with spaces. It is not a definitive solution, but it fixes it in the cd module.
  - Solution to the Windows directory path format in ASPX (now everything comes out as "/" instead of "\").
  - Fix bug in NET whoami module when impersonating a query for current privileges. A refactoring has been performed in this module to improve his usage.
  - Fix bug in NET execute_assembly module when passing multiple args to NET Assembly loaded.
  - Fix bug in NET execute module when process execution failed and can not read output from stdout/stderr (wait indefinitely).
  - Exception handling has been improved to avoid unexpected errors or ugly traceback exceptions.
- New core features:
  - Core command "rev2self" to revert to the user's original state on impersonation with an access token.
  - The help command has been modified to show information about the authors of the commands.
  - Added templates for creating modules: in PHP, JSP and ASPX.
  - New token system that allows impersonating users in the ASPX agent.
  - GZIP compression has been added to the process of encryption and decryption of the modules by the agents:
    - This makes it possible to encapsulate in GET (for example) and other fields of each method.
    - Significant reduction of module size.
  - New changes to connection profiles:
    - GET and POST can now be used.
    - Can encapsulate in any field (HEADER, FIELD and COOKIE) in GET and POST.
    - Skip TLS support.
  - Refactorisations of practically all modules in PHP, JSP and (above all) ASPX.
  - New shell format to a more common and intuitive one (based on the structure of any Linux shell).
  - Adding colors and some improvements to shell functionality.
- New features in ASPX Agent:
  - Now the module parameters are passed directly to the instantiated object from the agent. This is an improvement because, apart from reducing the module compilation size, it avoids that, in certain modules (like execute_assembly), the parameters are detected when injecting them to the module (because the "runtime compiling" writes the module to a temporary directory).
  - The functionality of impersonation with agent access tokens has been added. This way, when stealing a token and using it from the agent, you can impersonate the identity of the user of the stolen token and execute the module as that user (for example, SYSTEM after elevating privileges).
- New modules:
  - "dump_iis_secrets": module that allows to extract the credentials of different Application Pools identities in an IIS.
  - "dup_token": module (which replaces elevate_winlogon module and extends his functionality) to duplicate windows access tokens from processes.
  - "execute_as": module to execute a process using a primary token to impersonate access token identity (thanks to [specterops post](https://posts.specterops.io/understanding-and-defending-against-access-token-theft-finding-alternatives-to-winlogon-exe-80696c8a73b)).
  - "execute_assembly": module to load NET Assemblies directly into memory and invoke a method.
  - "impersonate": module to leak an access token from user (to impersonate in future) passing a credential as argument.
  - "list_tokens": module to list the windows access tokens accessible from the agent process based on the tool [Hanshell.aspx](https://github.com/blackarrowsec/redteam-research/blob/master/Hanshell/Hanshell.aspx) from Kurosh's post in [Blackarrow](https://www.tarlogic.com/blog/token-handles-abuse/).
  - "powerpick": module to execute unmanaged powershell using Runspaces from System.Management.Automation (only can execute powershell core commands for now).
  - "secretsdump": module to extract the keys: LSA and SECURITY, from the registry using Transacted Files to avoid touching disk and being detected (this module needs to be executed as SYSTEM).
  - "set_token": module to set an access token and impersonate the identity of the user it belongs to.
  - "show_integrity": module to show the integrity in the agent's current Thread.
  - "whoami": module to list user information, groups and privileges in Windows.

## [v0.3.0] - 2022-09-16

- The operating modes have been added (Standard and C2).
  - PHP Agent in C2 mode completed (JSP and ASP NET pending).
  - Substantial changes to most core files.
  - Minor changes to some commands.
- Restructuring of the Wiki with different sections.

## [v0.2.0] - 2022-09-07

- Fixed some bugs on modules:
  - Upload
    - When the file size is a multiple of the chunk size, the write was not done properly in Java and, in Php and Cs, an extra request was made.
  - Ls
    - In Php, an unexpected error occurred when the "file num links" of a file could not be obtained.
  - Cat  
    - In Cs, an uncaught exception was thrown when the target file could not be read.
  - Cp
    - In Java, exceptions not caught by an error message have been corrected so as not to break execution.
    - In Cs, an uncaught exception was thrown when a file could not be copied.
  - Cd
    - In Java and PHP, cwd for windows versions was not returning correctly.
  - Execute
    - A correction has been made to the PHP, CS and Java modules which, in principle, should work correctly (examples work). A specific dispatcher has been created for this command.
  - Tcpconnect
    - In Java, when the IP is not reachable, it used to take a long time to get the error, now it is determined on the fly.
- Fixed a bug that was detected in Windows when the encoding was not UTF-8.
- Fixed bad syntax on command examples in config file.
- A debug function has been added that writes the request information to disk.

## [v0.1.0] - 2022-09-01

- Refactored the PHP, JAVA and CS agents
- New message passing between client and agents
- Refactoring of the HTTP client
  - Connection profiles for agent communication
  - Possibility to encapsulate in any HTTP field
  - Possibility to build a custom HTTP request
  - Error handling
- Docker related refactorings
  - Java agents pre-compile all modules at startup (faster first load)
  - Container is stopped and removed at the end of each console run
- New distribution of environments to deploy Docker containers
- Module Refactoring
  - PHP Modules
    - The following commands work in any version: `5.x, 7.x, 8.x`
      - cat
      - cd
      - chmod
      - cp
      - download
      - execute
      - find
      - grep
      - id
      - ls
      - netstat
      - ps
      - rm
      - sysinfo
    - The following commands work in any version: `>=5.3, 7.x, 8.x`
      - touch
    - The following commands work in any version: `>=5.2, 7.x, 8.x`
      - upload
  - JAVA Modules
    - The following commands work in any of the Java versions: `1.7, 1.8`
      - cat
      - cd
      - cp
      - download
      - execute
      - id
      - ls
      - rm
      - sysinfo
      - tcpconnect
      - touch
      - upload
  - CS Modules
    - The following commands work in any version of the .NET Framework: `4.x`
      - cat
      - cd
      - cp
      - download
      - execute
      - id
      - ls
      - ps
      - rm
      - sysinfo
      - touch
      - upload
