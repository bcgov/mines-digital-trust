## GitHub Pages

We are using [GitHub Pages](https://pages.github.com) with [gh-pages branch](https://help.github.com/en/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#choosing-a-publishing-source) publishing source.  We have set gh-pages as the default branch and we require that all changes are done via Pull Requests.  However, in order to review/preview the changes, one must run the site locally.

## Content

The site is built with [Jekyll](https://jekyllrb.com), so start by reviewing their documentation.  Jekyll in turn uses [Markdown](https://daringfireball.net/projects/markdown/), [Liquid](https://github.com/Shopify/liquid/wiki), HTML & CSS to generate the static site.

### Collections

The site uses multiple pages, some of which are built from collections.
See the `collections` key in the config.yaml

[/collections](./collections) is the directory that collections go in.

[/collections/_services](./collections/_services) is the most likely spot to need to add new collections. Markdown files added here with the correct Front Matter will dynamically create the new pages, their navigation items, and add to lists on multiple pages.

### Publishing

GitHub Pages understands Jekyll and will build and deploy sites automatically, do **not** check in the *_site* directory.

1. Fork the [Mines Digital Trust repository](https://github.com/bcgov/mines-digital-trust)
2. Cd docs directory
3. Checkout gh-pages branch
4. Create branch from gh-pages
5. Add new collections (services), or other content
6. Build with Jekyll
7. Review your changes
8. Commit and push your changes to your fork.
9. Make a [Pull Request](https://github.com/bcgov/mines-digital-trust/pulls) in Mines Digital Trust repository.
10. Ask for a review and approval of changes.

## Build with Jekyll

1. Install a full Ruby development environment (2.6 works).
For Windows users, visit <https://rubyinstaller.org/downloads/> and download latest version WITH Devkit option. Install the installer (when prompted, just tap enter to use defaults - may happen twice)

1. Install [Jekyll](https://jekyllrb.com) and bundler gems.
Open a console window with directory at root of this repo and run:

```sh
gem install bundler
gem install jekyll
bundle install
```

1. Build and serve site (locally)

```sh
bundle exec jekyll build
bundle exec jekyll serve
```

1. Go to site: <http://localhost:4000/mines-digital-trust/>
