PyCommonist **v1.2** — batch upload to Wikimedia Commons.

Security and quality release, preparing the project for archiving.

- Hardened Commons API client: descriptive User-Agent, explicit timeouts,
  `assert=user` on authenticated calls, bot-password support, no credentials
  or tokens in logs
- Clear sign-in error messages (two-factor / bot-password hint)
- Show/hide password toggle and security hint in the auth panel
- Filename-existence check via the Commons API
- Fixed a crash when closing the application with open sessions
- User interface and documentation in English
- Offscreen smoke test: `QT_QPA_PLATFORM=offscreen python scripts/smoke_test.py`

See [History.md](../docs/archives/History.md) for the full contribution history.
