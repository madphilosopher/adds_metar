README.html: README.md
	pandoc -f markdown_github README.md -o README.html

clean:
	rm -f README.html
