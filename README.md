PHP Server Container Image For Wordpress
======================================

This repository is a fork from https://github.com/sclorg/s2i-php-container.git.

The original "README.md" ( "repo forked" ) is [README.md](.github/README_ORIGINAL.md)

The repository is part of a project ( "Laboratory Environment for Wordpress")  whose objective  is to create a laboratory environment to work through Openshit 3.11 on a website created with Wordpress. In this repository we create container image mysql database for Wordpress based on Centos7.

This is not a project of collaboration with "sclorg/s2i-php-container", so the master branch used just to keep this repository up to date. For more information about working to repository to see [aquí](.github/WORKFLOW.md). 

# Getting Started 

We create a custom container with s2i-php in centos7 system. For this we use [source-to-image](https://github.com/openshift/source-to-image) technology.

We create two branches:
- "main" what is the production
- "develop" which is the development

## Prerequisites
   - Openshift 3.11
   - git
   - github
   - you want
   
# Running the tests
 
 The tests are developed in openshitf and we will not show their development and performance. If we note that we will do individualized tests for each image and a global one with all the images at play (wordpress and mysql).
 
# Contributing

In principle it is a personal and public project.

# Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

# Authors

    . jemiliolopez - Initial work - PurpleBooth


# License

This project is licensed under the APACHE License original - see the LICENSE file for details

# Acknowledgments
 To all, who are many and anonymous, who have contributed their knowledge and experience by sharing it with people.

 
 
 
   
   

