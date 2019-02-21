


| Code | Description |
| ---- | ---- |
| Positive completion reply ||
| 211 | System status or system help reply. |
| 214 | Help message. |
| 220 | Domain service ready. |
| 221 | Domain service closing transmission channel. |
| 235 | Authentication successful. |
| 250 | Requested command completed. |
| 251 | User not local, so the command will be forwarded. |
| 252 | Cannot verify user, but will attempt delivery. |
|||
| Positive intermediate reply ||
| 334 | Server authentication challenge. |
| 354 | Start mail input. |
|||
| Transitive negative completion reply ||
| 421 | Domain service not available, closing transmission channel. |
| 450 | Mailbox unavailable. |
| 451 | Local error in processing: command aborted. |
| 452 | Insufficient system storage: command aborted. |
| 453 | No mail available. |
|||
| Permanent negative completion reply ||
| 500 | Command not recognised: syntax error. |
| 501 | Syntax error in parameters or arguments. |
| 502 | Command not implemented. |
| 503 | Bad sequence of commands. |
| 504 | Command parameter temporarily not implemented. |
| 534 | Authentication mechanism is too weak. |
| 538 | Encryption required for requested authentication mechanism. |
| 550 | Requested action not taken: mailbox unavailable. |
| 551 | User not local |
| 552 | Requested mail action aborted: exceeded storage allocation. |
| 553 | Requested mail action not taken: mailbox name not allowed. |
| 554 | Transaction failed. |
