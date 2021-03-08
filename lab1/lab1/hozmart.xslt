<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml"
                doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"
                doctype-public="-//W3C//DTD XHTML 1.1//EN" indent="yes"/>

  <xsl:template match="/">
    <html>
      <head>
        <title>
          Saws
        </title>
      </head>
      <body>
        <h1>
          Saws
        </h1>
        <table>
          <tr>
            <td>Name</td>
            <td>Price</td>
            <td>Availability</td>
          </tr>
          <xsl:apply-templates/>
        </table>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="product">
    <tr>
     <td>
         <xsl:value-of select="name"/>
         <br/>
         <xsl:element name="image">
             <xsl:attribute name="src">
                 <xsl:value-of select="image"/>
             </xsl:attribute>
         </xsl:element>
     </td>
     <td><xsl:value-of select="price"/></td>
     <td><xsl:value-of select="availability"/></td>
    </tr>
  </xsl:template>

</xsl:stylesheet>