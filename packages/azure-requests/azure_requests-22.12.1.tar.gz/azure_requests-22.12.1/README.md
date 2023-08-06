# Azure requests

Just a wrapper around Python requests module for communicating with Azure DevOps.

## DRY (don't repeat yourself) features

- Authentication
- Replace organization, project, and team in URL, so URLs can be copy-pasted from the documentation
- Handle rate limit
- Handle ADO temporary server errors
- Set appropriate Content-Type headers
- Parse JSON automatically
- Raise exception for wrong HTTPS statuses

## Rationale

Azure DevOps has an excellent HTTPS API with an excellent documentation. It is easy to understand and easy to use. For smaller scripts and projects it is easier to use them as is. Every existing API implementations have many documentation issues.
