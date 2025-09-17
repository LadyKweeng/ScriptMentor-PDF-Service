# Enhanced PDF Parsing Features

## 🎯 Overview

The PDF parsing system has been significantly enhanced with intelligent title page detection and screenplay start identification. This ensures that parsing begins at the actual screenplay content, not title pages.

## 🚀 New Features

### 1. Enhanced Title Page Detection (`utils/title_page_detector.py`)

#### **Multi-Strategy Detection System**
The system uses 4 detection strategies in order of preference:

1. **Explicit PAGE 1 Markers**
   - Detects: `PAGE 1`, `1.`, `- 1 -`, `[1]`, `(1)`, `1/120`, `Page 1 of 120`
   - Most reliable method when present

2. **Screenplay Opening Pattern Detection**
   - Detects common screenplay openings in first 20 lines of each page
   - Patterns include: `FADE IN`, `OVER BLACK`, `INT.`, `EXT.`, `COLD OPEN`, etc.

3. **Content Analysis Scoring**
   - Calculates "title page probability" for each page
   - Considers pattern density, line length, whitespace ratio
   - Score: 0.0 = screenplay content, 1.0 = title page

4. **Fallback Detection**
   - If first page contains typical title page elements, skip it
   - Ensures parsing starts from screenplay content

#### **Comprehensive Pattern Recognition**

**Title Page Patterns Detected:**
- Contact information (emails, phones, addresses)
- Dates and version information
- Copyright and legal notices
- Credits ("Written by", "Screenplay by", etc.)
- Production information
- Character lists and cast pages
- Agent/representative information
- WGA registration info

**Screenplay Opening Patterns:**
- **Transitions:** `FADE IN`, `FADE IN:`, `FADE IN --`, `FADE UP`, `OVER BLACK`
- **Scene Headings:** `INT.`, `EXT.`, `INT/EXT.`, `I/E.`, `INTERIOR`, `EXTERIOR`
- **Special Opens:** `COLD OPEN`, `TEASER`, `PRE LAP`, `TITLE CARD:`, `SUPER:`
- **Time Indicators:** `CONTINUOUS`, `LATER`, `MOMENTS LATER`, `THE NEXT DAY`
- **Montages:** `BEGIN MONTAGE`, `SERIES OF SHOTS:`, `SEQUENCE:`
- **Commercial:** `OPEN ON:`, `WE OPEN ON`, `WE SEE`, `STOCK FOOTAGE`

### 2. Enhanced Main Parser Integration

#### **Modified `_extract_pages()` Method**
```python
# NEW: 5-step enhanced extraction process
1. Extract all pages from PDF
2. Run title page detection analysis
3. Filter to screenplay content only
4. Renumber pages starting from 1
5. Log detailed detection results
```

#### **Smart Page Management**
- Preserves original page numbers as `original_page_num`
- Renumbers screenplay pages as `screenplay_page_num`
- Maintains `page_num` as screenplay page number for consistency

#### **Enhanced Logging**
```
📄 Extracted 5 total pages from PDF
📋 Title page detection: Explicit PAGE 1 marker found: 'PAGE 1'
⏭️  Skipped 2 title page(s), starting screenplay from original page 3
📖 Processing 3 screenplay pages (renumbered 1-3)
```

## 📊 Detection Examples

### ✅ **Successfully Detected Title Pages**
- Production company pages with logos and contact info
- "Written by" pages with author credits
- Character list pages
- Copyright and legal pages
- Cast pages with character descriptions

### ✅ **Successfully Detected Screenplay Starts**
- `FADE IN:` - Classic screenplay opening
- `OVER BLACK` - Modern screenplay opening
- `INT. HOUSE - DAY` - Direct scene heading start
- `PAGE 1` marker with scene following
- `COLD OPEN` - TV script opening

### ✅ **Edge Cases Handled**
- PDFs with multiple title pages
- Scripts that start mid-scene with `CONTINUOUS`
- Commercial scripts starting with `OPEN ON:`
- Scripts with pre-lap audio (`PRE LAP:`)

## 🔧 Technical Implementation

### **Class Structure**
```python
TitlePageDetector()
├── detect_title_pages() → (start_index, reason)
├── _detect_explicit_page_1() → Look for PAGE 1 markers
├── _detect_screenplay_opening() → Find screenplay patterns
├── _analyze_title_page_content() → Content scoring analysis
└── _calculate_title_page_score() → Probability calculation
```

### **Integration Points**
```python
ScreenplayParser.__init__()
└── self.title_page_detector = TitlePageDetector()

ScreenplayParser._extract_pages()
├── Extract all pages
├── screenplay_start_index, reason = self.title_page_detector.detect_title_pages()
└── Return screenplay_pages[screenplay_start_index:]
```

## 📈 Expected Improvements

### **Parsing Accuracy**
- ✅ Eliminates title page noise from screenplay analysis
- ✅ Ensures character detection starts from actual dialogue
- ✅ Improves scene structure analysis
- ✅ Better format compliance scoring

### **User Experience**
- ✅ More accurate page counts (screenplay pages only)
- ✅ Proper scene numbering from actual start
- ✅ Cleaner character lists without title page text
- ✅ Better dialogue extraction quality

### **Edge Case Handling**
- ✅ Works with single or multiple title pages
- ✅ Handles PDFs without title pages gracefully
- ✅ Adapts to different screenplay formats
- ✅ Maintains backward compatibility

## 🚦 Status

- ✅ **Title Page Detector**: Implemented and tested
- ✅ **Main Parser Integration**: Complete
- ✅ **Pattern Recognition**: Comprehensive coverage
- ✅ **Logging and Debugging**: Enhanced visibility
- 🔄 **Ready for Deployment**: All features functional

## 🔮 Future Enhancements

Potential areas for future development:
- ML-based title page classification
- Support for international screenplay formats
- Enhanced commercial script pattern recognition
- Integration with scene analysis for better start detection

---

*Last Updated: $(date)*
*Version: 1.0 - Enhanced Title Page Detection*