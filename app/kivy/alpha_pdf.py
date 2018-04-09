from fpdf import FPDF
from fpdf.php import substr, sprintf, print_r

class AlphaPDF(FPDF):
    extgstates = {}

    # alpha: real value from 0 (transparent) to 1 (opaque)
    # bm:    blend mode, one of the following:
    #          Normal, Multiply, Screen, Overlay, Darken, Lighten, ColorDodge, ColorBurn,
    #          HardLight, SoftLight, Difference, Exclusion, Hue, Saturation, Color, Luminosity
    def set_alpha(self, alpha, bm='Normal'):
        # set alpha for stroking (CA) and non-stroking (ca) operations
        gs = self.AddExtGState({'ca':alpha, 'CA':alpha, 'BM':'/'+bm})
        self.SetExtGState(gs)

    def AddExtGState(self, parms):
        n = len(self.extgstates)
        if n not in self.extgstates:
            self.extgstates[n] = {}
        self.extgstates[n]['parms'] = parms
        return n

    def SetExtGState(self, gs):
        self._out(sprintf('/GS%d gs', gs))

    def _enddoc(self):
        if self.extgstates and self.pdf_version<'1.4':
            self.pdf_version='1.4'
        FPDF._enddoc(self)

    def _putextgstates(self):
        for i in range(len(self.extgstates)):
            self._newobj()
            self.extgstates[i]['n'] = self.n
            self._out('<</Type /ExtGState')
            parms = self.extgstates[i]['parms']
            self._out(sprintf('/ca %.3F', parms['ca']))
            self._out(sprintf('/CA %.3F', parms['CA']))
            self._out('/BM '+parms['BM'])
            self._out('>>')
            self._out('endobj')

    def _putresourcedict(self):
        FPDF._putresourcedict(self)
        self._out('/ExtGState <<')
        for k,extgstate in self.extgstates.items():
            self._out('/GS'+str(k)+' '+str(extgstate['n'])+' 0 R')
        self._out('>>')

    def _putresources(self):
        self._putextgstates()
        FPDF._putresources(self)
