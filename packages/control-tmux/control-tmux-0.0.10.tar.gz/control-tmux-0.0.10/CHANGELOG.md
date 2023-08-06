[Version 0.0.10 (2022-12-18)](https://pypi.org/project/control-tmux/0.0.10/)
=============================

* Make sure ~/.local/bin is in path if `control-tmux` is installed there ([f3c4f9e](https://gitlab.com/ktpanda/control-tmux/-/commit/f3c4f9e1566584d2913189beb94f563f93bf3c72))


[Version 0.0.9 (2022-12-05)](https://pypi.org/project/control-tmux/0.0.9/)
============================

* Fix _add_prompt_command so that commands are added in reverse order ([e787805](https://gitlab.com/ktpanda/control-tmux/-/commit/e787805fcf31aeac2bf06ea2dce2b42ca254d64f))


[Version 0.0.8 (2022-10-29)](https://pypi.org/project/control-tmux/0.0.8/)
============================

* usersetup: Use shell functions instead of aliases for command shortcuts ([28a672c](https://gitlab.com/ktpanda/control-tmux/-/commit/28a672c814ff5c7b8abaf097f173cb0ed4b53939))


[Version 0.0.7 (2022-10-12)](https://pypi.org/project/control-tmux/0.0.7/)
============================

* Remove stray '/' left in PROMPT_COMMAND after restoring ([b0f486c](https://gitlab.com/ktpanda/control-tmux/-/commit/b0f486ceb83e9ea41c0ac156d09cfef5664303a9))


[Version 0.0.6 (2022-10-11)](https://pypi.org/project/control-tmux/0.0.6/)
============================

* Fix 'control-tmux -s all' ([0f5bdc3](https://gitlab.com/ktpanda/control-tmux/-/commit/0f5bdc3af260d11296a5038b8266e1f21fe49c3f))
* Update README.html ([23eb7eb](https://gitlab.com/ktpanda/control-tmux/-/commit/23eb7ebcefcc709ffb76899d93b970bcba07956d))


[Version 0.0.5 (2022-10-06)](https://pypi.org/project/control-tmux/0.0.5/)
============================

* Update instructions in README.md ([c3c3f7a](https://gitlab.com/ktpanda/control-tmux/-/commit/c3c3f7aa4d7eaaae8b33083ff192be3b1cbd2ce8))


[Version 0.0.4 (2022-09-26)](https://pypi.org/project/control-tmux/0.0.4/)
============================

* Treat empty TMUX variables as not present ([ac8e65c](https://gitlab.com/ktpanda/control-tmux/-/commit/ac8e65cc66439e7f45bb37d815ac87a4adaa5b4e))


[Version 0.0.3 (2022-09-26)](https://pypi.org/project/control-tmux/0.0.3/)
============================

* Fix bugs with sock_dir ([1d855e9](https://gitlab.com/ktpanda/control-tmux/-/commit/1d855e918a71250ce6412b7aa532115c1961b5d4))


[Version 0.0.2 (2022-09-26)](https://pypi.org/project/control-tmux/0.0.2/)
============================

* Add --setup option and argcomplete support ([83cb960](https://gitlab.com/ktpanda/control-tmux/-/commit/83cb96089528d25bbf04fd829d8d78cb0932240a))
* Refactor to use pathlib and clean up ([239c8ce](https://gitlab.com/ktpanda/control-tmux/-/commit/239c8ce98f0d6885274c83a0fcedc02a265b82ed))


[Version 0.0.1 (2022-09-26)](https://pypi.org/project/control-tmux/0.0.1/)
============================

* Convert to using setuptools ([6229cb7](https://gitlab.com/ktpanda/control-tmux/-/commit/6229cb702a3529ca27af6191e6825a4b995f5b8a))


Version 0.0.0
============================

* Add preliminary support for remote tmux sessions ([51ff8ac](https://gitlab.com/ktpanda/control-tmux/-/commit/51ff8ac43801bb61d41108b98cb1b9cdb1e6e290))
* Clean up PROMPT_COMMAND after restore ([5103ef0](https://gitlab.com/ktpanda/control-tmux/-/commit/5103ef0e68072eeb3da54f4c573d503c0d5e225e))
* Update installer to support .bashrc.d ([f660e48](https://gitlab.com/ktpanda/control-tmux/-/commit/f660e48fc912255126362411931215c0d3b2e54a))
* Update tmux.setup.sh to be more compatible and make it idempotent ([70e5e27](https://gitlab.com/ktpanda/control-tmux/-/commit/70e5e2704d61df619732110675f69eff5cb37af3))
* Actually add tmux.default.conf-tmux-2.0 this time ([5dc7af9](https://gitlab.com/ktpanda/control-tmux/-/commit/5dc7af99dcccba36d5aced624b2d101c0a66a56e))
* Author name change ([5a183a8](https://gitlab.com/ktpanda/control-tmux/-/commit/5a183a874072ca0fd43bae100fb481785656ab7f))
* Install newer tmux.default.conf ([3fbfde8](https://gitlab.com/ktpanda/control-tmux/-/commit/3fbfde868be26ca20b1753906750a792ba6dae92))
* Use a sequence of ASCII characters as a separator instead of a control character ([d1de856](https://gitlab.com/ktpanda/control-tmux/-/commit/d1de8565af7d8fc19406fbefcd22890a03607c11))
* Limit length of command line sent to tmux when restoring sessions ([898659a](https://gitlab.com/ktpanda/control-tmux/-/commit/898659a30e2097f2b1931fa30f9a88062cb0f8be))
* Initial commit ([3a5c986](https://gitlab.com/ktpanda/control-tmux/-/commit/3a5c9864774afbd796c25edc816043bf0aa4221c))
