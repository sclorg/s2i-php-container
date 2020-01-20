Workflow
==========

## Project: Laboratory Environmet for Wordpress
### Organización: devnely-org
### Product Manager: S2i-Php
### Forked site: https://github.com/sclorg/s2i-php-container.git
### Dev site: https://github.com/devnely-org/s2i-php-container.git
### Branch deployed on dev site: main
### Branch development on dev site: develop
### Live site:  https://github.com/devnely-org/s2i-php-container.git
### Branch deployed on live site: main
### Branch development on live site: develop
### When starting a dev ticket, branch from: [#number_issue]_[ticket]
### When starting a hotfix ticket, branch from: [#number_issue]_[hotfix]

### Content commit

- (50 characters) Subject
- (72 characters) Problem (problem,task,reason for commit)
- Solution (solution and list of changes)
- ticket or issue
- note




### When updating your work, use: 

1.  `git checkout master`
2.  `git pull sclorg master --rebase=preserve` (upstream remote)
3.  `git diff FETCH_HEAD`
4.  `git merge`
5.  `git submodule update --init` (sure initial commit)
6.  `git checkout develop`
7.  `git pull sclorg master --rebase=preserve`
8.  `git rebase master`
9.  `git checkout master`
10. `git merge develop`




### When merging your work post review, use: 

1.  `git checkout master`
2.  `git pull sclorg master --rebase=preserve` (upstream remote)
3.  `git diff FETCH_HEAD`
4.  `git merge`
5.  `git submodule update --init` (sure initial commit)
6.  `git checkout develop`
7.  `git pull sclorg master --rebase=preserve`
8.  `git rebase master`
9.  `git checkout master`
10. `git merge develop`


