# Short Form Content Engine public compliance site

Static GitHub Pages site for the private desktop creator workflow. This repository contains public product/policy information only; no application source, credentials or upload records belong here.

## Stable URLs

- Home: https://brown-9058.github.io/short-form-content-engine-compliance/
- TikTok integration: https://brown-9058.github.io/short-form-content-engine-compliance/tiktok/
- TikTok privacy: https://brown-9058.github.io/short-form-content-engine-compliance/tiktok/privacy/
- TikTok terms: https://brown-9058.github.io/short-form-content-engine-compliance/tiktok/terms/
- Existing YouTube/API privacy: https://brown-9058.github.io/short-form-content-engine-compliance/privacy.html
- Existing YouTube/API terms: https://brown-9058.github.io/short-form-content-engine-compliance/terms.html

GitHub Pages serves `main` at the repository root. `.nojekyll` keeps these files static. Do not rename existing policy URLs, move verification files or regenerate the TikTok verification signature.

## Local validation and preview

Run `python3 scripts/validate_site.py`. No build, dependencies or JavaScript are required.
For a preview with the same project URL prefix, run `python3 -m http.server 8765 --directory ..` from this repository and open `http://localhost:8765/short-form-content-engine-compliance/`.

The Developer Portal configuration includes `user.info.basic` and `video.upload`. The current local adapter only requests `video.upload` and confirms the identifier returned by OAuth; the site explicitly distinguishes configured basic-profile permission from implemented profile retrieval. Do not claim production approval, public availability or Direct Post functionality. Local captions/credits remain creator suggestions, not upload API fields.

Deployment: commit only public site changes and push this repository's `main` branch. Verify all stable URLs and the unchanged root verification file after GitHub Pages finishes deploying. Do not copy or publish the private application repository. Contact: ethan@ibrowns.com.
