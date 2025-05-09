<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:strip-space elements="*"/> <!-- Убирает лишние пробелы/переносы строк -->

    <xsl:template match="/music_library">
        <xsl:text>МУЗЫКАЛЬНАЯ БИБЛИОТЕКА
========================

</xsl:text>
        <xsl:apply-templates select="album"/>
    </xsl:template>

    <xsl:template match="album">
        <xsl:text>Альбом: </xsl:text>
        <xsl:value-of select="title"/>
        <xsl:text> (</xsl:text>
        <xsl:value-of select="release_date"/>
        <xsl:text>, </xsl:text>
        <xsl:value-of select="age_restriction"/>
        <xsl:text>)
</xsl:text>

        <xsl:text>Исполнители: </xsl:text>
        <xsl:for-each select="artists/artist">
            <xsl:value-of select="."/>
            <xsl:if test="position() != last()">, </xsl:if>
        </xsl:for-each>
        <xsl:text>
</xsl:text>

        <xsl:text>Жанры: </xsl:text>
        <xsl:for-each select="genres/genre">
            <xsl:value-of select="."/>
            <xsl:if test="position() != last()">, </xsl:if>
        </xsl:for-each>
        <xsl:text>
</xsl:text>

        <xsl:text>Композиции:
</xsl:text>
        <xsl:for-each select="compositions/composition">
            <xsl:text>  - </xsl:text>
            <xsl:value-of select="name"/>
            <xsl:text> (</xsl:text>
            <xsl:value-of select="duration"/>
            <xsl:text>)
</xsl:text>
        </xsl:for-each>
        <xsl:text>------------------------

</xsl:text>
    </xsl:template>

</xsl:stylesheet>