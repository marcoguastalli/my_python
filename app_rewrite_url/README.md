# App Rewrite Url

This is the syntax of a Rewrite Rule https://cwiki.apache.org/confluence/display/HTTPD/RewriteRule:
`RewriteRule pattern substitution [flags]`

Steps:
- read a txt file that contains n patterns
- read a txt file that contains n substitutions
- create a txt file that contains n Rewrite Rules
- the number of entries in both files must match
