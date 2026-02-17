# Deploying this static site to Azure Static Web Apps

Deploy 1 
Steps to deploy:

1. Create an Azure Static Web App resource in the Azure Portal or via the CLI. Use the repository you will push from (GitHub).

2. In the Azure portal, when creating the Static Web App, choose the repository and branch (the workflow currently targets `main`).

3. Azure will create a GitHub Actions workflow automatically if you configure it through the portal. If you prefer to add it manually, a workflow file has been added at `.github/workflows/azure-static-web-apps.yml` — adjust the `branches` entry if you use a different branch.

4. Add the deployment token (if you didn't let Azure create the workflow automatically) as a repository secret named `AZURE_STATIC_WEB_APPS_API_TOKEN`. You can get this token from the Azure Static Web App resource -> Manage deployment token.

5. The site root is the repo root. The workflow uploads the files at the repo root as the app content (`app_location: /`, `output_location: /`).

Notes and recommendations:
- The project uses relative asset paths (e.g. `wp-content/...`), which are compatible with Azure Static Web Apps when served from the repository root.
- `staticwebapp.config.json` was added to provide a navigation fallback to `index.html` while excluding common static asset directories (so images, CSS and JS are served normally).
- If you want each subfolder's `index.html` to act as a separate route (e.g. `/about-us/`), those already exist as files in the repository and will be served normally.
- If your production site relies on WordPress/PHP server APIs (xmlrpc, admin-ajax endpoints, server-side forms), those will not run on Azure Static Web Apps as-is — you will need server-side replacements (APIs) or host dynamic parts elsewhere.

Troubleshooting:
- If you use a branch other than `main`, update the workflow file branch list or change the branch in the Azure Static Web App creation flow.
- If you see 404s for client-side routes, confirm `staticwebapp.config.json` navigationFallback excludes the correct asset patterns.
