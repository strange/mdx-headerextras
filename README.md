A simple module that creates id's from the heading's text (excluding any HTML)
and can adjust the starting level of headings.

Example:
    subject = "# What a nice day!"
    html = markdown.markdown(subject,
                             ['headerextras(level=3, prefix=section-)'])

    # <h2 id="section-what-a-nice-day">What a nice day!</h2>
