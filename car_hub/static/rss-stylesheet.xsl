<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="/static/rss-stylesheet.xsl"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html>
        <head>
            <title>Latest Cars RSS Feed</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    margin: 0;
                    padding: 20px;
                }
                h1 {
                    color: #343a40;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #343a40;
                    color: white;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                tr:hover {
                    background-color: #ddd;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Latest Cars RSS Feed</h1>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
                    <xsl:for-each select="rss/channel/item">
                        <tr>
                            <td><xsl:value-of select="title"/></td>
                            <td><xsl:value-of select="description"/></td>
                            <td><a href="{link}" target="_blank">View</a></td>
                        </tr>
                    </xsl:for-each>
                </tbody>
            </table>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>