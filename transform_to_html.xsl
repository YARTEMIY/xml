<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>

    <xsl:template match="/music_library">
        <html>
            <head>
                <title>Музыкальная Библиотека</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
                    h1 { color: #333; text-align: center; }
                    table { width: 90%; margin: 20px auto; border-collapse: collapse; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                    th { background-color: #4CAF50; color: white; }
                    tr:nth-child(even) { background-color: #f9f9f9; }
                    tr:hover { background-color: #f1f1f1; }
                    .compositions-list { list-style-type: none; padding-left: 0; }
                    .compositions-list li { padding: 3px 0; }
                </style>
            </head>
            <body>
                <h1>Музыкальная Библиотека</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Название Альбома</th>
                            <th>Исполнители</th>
                            <th>Жанры</th>
                            <th>Дата Выхода</th>
                            <th>Возраст. огр.</th>
                            <th>Композиции (Длительность)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:apply-templates select="album"/>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="album">
        <tr>
            <td><xsl:value-of select="title"/></td>
            <td>
                <xsl:for-each select="artists/artist">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()"><br/></xsl:if>
                </xsl:for-each>
            </td>
            <td>
                <xsl:for-each select="genres/genre">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()"><br/></xsl:if>
                </xsl:for-each>
            </td>
            <td><xsl:value-of select="release_date"/></td>
            <td><xsl:value-of select="age_restriction"/></td>
            <td>
                <ul class="compositions-list">
                    <xsl:for-each select="compositions/composition">
                        <li>
                            <xsl:value-of select="name"/> (<xsl:value-of select="duration"/>)
                        </li>
                    </xsl:for-each>
                </ul>
            </td>
        </tr>
    </xsl:template>

</xsl:stylesheet>