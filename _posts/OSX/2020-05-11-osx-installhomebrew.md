---
title : macOS 패키지 관리자 Homebrew 설치 및 사용하기
tags :
- brew
- Homebrew
- macOS
categories:
- OS X
toc: true
toc_min: 1
toc_max: 4
toc_sticky: true
toc_label: "On This Page"
author_profile: true
---

홈브루(Homebrew)는 자유-오픈 소스 소프트웨어 패키지 관리 시스템입니다. 개발자 입장에서 맥 OS 를 사용하면 얻게되는 큰 이점중 하나가 이 Homebrew 입니다.

설치 사이트입니다.

https://brew.sh/index_ko 접속하셔서 그대로 터미널에 붙여넣기 하면 됩니다.

![image](https://user-images.githubusercontent.com/44635266/80797493-ed635f00-8bdc-11ea-83f1-0977fd2c9b3d.png)

명령어는 아래와 같습니다.

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

설치가 되는지 확인할 수 있습니다.

```shell
$ brew --version

Homebrew 2.2.13
Homebrew/homebrew-core (git revision 7429; last commit 2020-04-22)
Homebrew/homebrew-cask (git revision f3436; last commit 2020-04-22)
```

제 맥북에 설치되어있는 패키지들입니다. `cask` 는 GUI 라고 생각하시면 됩니다. 아래에서 확인할 수 있듯이 `google-chrome`, `visual-studio-code` 같은 개발툴도 이 Homebrew 로 설치가 가능합니다.

```shell
$ brew list
apache-spark		gettext			jupyterlab		mysql			pcre2			sqlite
curl			git			kafka			ncurses			postgresql		tree
docker			go			krb5			node			protobuf		xz
docker-compose		hadoop			libyaml			openssl@1.1		python			zeromq
ethereum		icu4c			maven			pandoc			readline		zookeeper
gdbm			ipython			mongodb-community	pcre			scala			zsh
```

```shell
$ brew cask list
dbeaver-community        font-hack-nerd-font      intellij-idea-ce         pgadmin4                 sequel-pro               tableplus
docker                   gitkraken                iterm2                   postman                  skype                    vagrant
eclipse-jee              google-chrome            macs-fan-control         pycharm-ce               springtoolsuite          visual-studio-code
```

찾고자 하는 패키지가 있으면 `search` 를 이용하면 됩니다.

```shell
$ brew search git

==> Formulae
bagit                    git-delta                git-multipush            git-sh                   gitbatch                 gitversion
bash-git-prompt          git-extras               git-now                  git-sizer                gitbucket                lazygit
cgit                     git-filter-repo          git-number               git-ssh                  giter8                   legit
digitemp                 git-fixup                git-octopus              git-standup              gitfs                    libgit2
easy-git                 git-flow                 git-open                 git-subrepo              gitg                     libgit2-glib
git ✔                    git-flow-avh             git-plus                 git-svn-abandon          github-keygen            literate-git
git-absorb               git-fresh                git-quick-stats          git-test                 github-markdown-toc      modgit
git-annex                git-ftp                  git-recent               git-tf                   github-release           moz-git-tools
git-annex-remote-rclone  git-game                 git-remote-codecommit    git-tig                  gitlab-gem               pass-git-helper
git-appraise             git-gerrit               git-remote-gcrypt        git-town                 gitlab-runner            pygitup
git-archive-all          git-gui                  git-remote-hg            git-tracker              gitleaks                 sagittarius-scheme
git-cal                  git-hooks                git-review               git-trim                 gitless                  stgit
git-cinnabar             git-if                   git-revise               git-url-sub              gitmoji                  topgit
git-cola                 git-imerge               git-secret               git-utils                gitslave                 ungit
git-credential-manager   git-integration          git-secrets              git-vendor               gitter-cli               willgit
git-crypt                git-lfs                  git-series               git-when-merged          gitup                    zsh-git-prompt
==> Casks
adobe-digital-editions   gitbox                   github-beta              gitter                   refined-github-safari    webplotdigitizer
deepgit                  gitee                    githubpulse              gitup                    rowanj-gitx
git-it                   giteye                   gitify                   gitx                     smartgit
gitahead                 gitfinder                gitkraken ✔              lego-digital-designer    snagit
gitblade                 gitfox                   gitnote                  logitech-presentation    snagit4
gitbook                  github                   gitscout                 plotdigitizer            subgit
```

내가 현재 설치된 패키지도 확인할 수 있습니다. 설치는 `brew install (package name)` 이나 `brew cask install (package name)` 을 입력하시면 됩니다.

예시로는 Github 를 설치해보겠습니다.

```shell
$ brew cask install github

pdating Homebrew...
==> Auto-updated Homebrew!
Updated 1 tap (homebrew/core).
==> Updated Formulae
jupyterlab ✔               netpbm                     texlab
pcre2 ✔                    nqp                        tmuxinator-completion
amqp-cpp                   oauth2_proxy               treefrog
bison                      open-babel                 ungit
clojure-lsp                opencc                     urdfdom_headers
contentful-cli             phpstan                    v8
couchdb                    plantuml                   vagrant-completion
gexiv2                     proteinortho               vale
git-quick-stats            proxytunnel                vapoursynth
glooctl                    pwntools                   vapoursynth-imwri
gnumeric                   python-markdown            vapoursynth-ocr
gnutls                     r                          vapoursynth-sub
goffice                    rakudo                     vfuse
gom                        ripgrep                    volta
katago                     rust                       vpn-slice
lc0                        semgrep                    wartremover
minimal-racket             sleuthkit                  webtorrent-cli
moarvm                     sonarqube                  weechat
mu                         tealdeer                   z3
mvnvm                      tengo
mvtools                    terragrunt

==> Downloading https://desktop.githubusercontent.com/releases/2.4.3-539849ed/Git
######################################################################## 100.0%
==> Verifying SHA-256 checksum for Cask 'github'.
==> Installing Cask github
==> Moving App 'GitHub Desktop.app' to '/Applications/GitHub Desktop.app'.
==> Linking Binary 'github.sh' to '/usr/local/bin/github'.
🍺  github was successfully installed!
```

삭제는 다음과 아래와같이 하면 됩니다.

```shell
$ brew cask uninstall github
```

마지막으로 설치 경로를 알려드리고 끝내겠습니다.

```shell
$ cd /usr/local/Cellar/
$ ls
apache-spark/      hadoop/            mysql/             python/
curl/              icu4c/             ncurses/           readline/
docker/            ipython/           node/              scala/
docker-compose/    jupyterlab/        openssl@1.1/       sqlite/
ethereum/          kafka/             pandoc/            tree/
gdbm/              krb5/              pcre/              xz/
gettext/           libyaml/           pcre2/             zeromq/
git/               maven/             postgresql/        zookeeper/
go/                mongodb-community/ protobuf/          zsh/
```

Cask 로 설치된 파일들은 아래에 저장됩니다.

```shell
$ cd /usr/local/Caskroom/
$ ls
dbeaver-community/   intellij-idea-ce/    sequel-pro/
docker/              iterm2/              skype/
eclipse-jee/         macs-fan-control/    springtoolsuite/
font-hack-nerd-font/ pgadmin4/            tableplus/
gitkraken/           postman/             vagrant/
google-chrome/       pycharm-ce/          visual-studio-code/
github/
```