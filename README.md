# Static compliance site

Not deployed. No secrets, source code, analytics or external scripts belong here.

1. Replace contact_email and public_site_url in site.toml. Use your chosen public contact email and final HTTPS Pages URL.
2. Obtain the official logo as instructed in assets/README.md.
3. From the private project: `.venv/bin/python scripts/build_compliance_site.py` then `youtube audit-readiness`.
4. Publish ONLY this directory in a separate public repository; never publish the private application repository.

Example user-operated deployment (replace YOUR_USER; run from the project root):

```sh
mkdir ../short-form-content-engine-compliance
cp -R compliance-site/. ../short-form-content-engine-compliance/
cd ../short-form-content-engine-compliance
git init -b main
git add .
git commit -m "publish compliance documentation"
gh repo create YOUR_USER/short-form-content-engine-compliance --public --source=. --push
gh api --method POST repos/YOUR_USER/short-form-content-engine-compliance/pages -f 'source[branch]=main' -f 'source[path]=/'
```

Final URL: `https://YOUR_USER.github.io/short-form-content-engine-compliance/`.
Check all links and logo, then capture evidence. No workflow is enabled here. The safe deployment option is GitHub Pages branch deployment above, which only copies static site files and needs no application secrets. Verify `git ls-files` in the new repo before pushing. Do not copy the private project itself.
