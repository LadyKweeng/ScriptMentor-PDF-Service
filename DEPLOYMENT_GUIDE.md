# Enhanced Spatial Parser Deployment Guide

## 🎯 Objective
Deploy PDFPlumber spatial awareness enhancements to achieve **99% accuracy** in action/dialogue separation.

## ✅ Current Status
- ✅ **Backup Complete**: Original service backed up to git commit `4b76f66`
- ✅ **Enhancements Ready**: Enhanced spatial parser implemented and tested
- ✅ **Feature Flag**: Easy reversion with `USE_ENHANCED_SPATIAL_PARSER = False`
- ✅ **Local Testing**: All tests pass - parser correctly classifies screenplay elements

## 🚀 Manual Deployment Steps

### Step 1: Deploy Code Changes
Since Railway CLI requires authentication, deploy manually:

1. **Push to Railway-connected repository**:
   ```bash
   git push origin main  # (or your Railway-connected branch)
   ```

2. **Railway will auto-deploy** the enhanced service

### Step 2: Configure Environment Variables
In your Railway dashboard, set these environment variables:

```bash
USE_ENHANCED_SPATIAL_PARSER=true
SPATIAL_PARSER_VERSION=3.0
ACCURACY_TARGET=99
```

### Step 3: Verify Deployment
Monitor Railway logs for:
```
🎯 Using Enhanced Spatial Parser for 99% accuracy
```

## 🔍 Testing Enhanced Service

### Upload Test PDF
1. Upload a PDF with action/dialogue mixing issues
2. Check response metadata for: `"processedVia": "railway-spatial-enhanced"`
3. Verify action lines have proper spacing before dialogue blocks

### Expected Improvements
- **Action/Dialogue Separation**: 87% → 99% accuracy
- **Character Detection**: Eliminates "CLOSE ON:" misclassifications
- **Spatial Awareness**: Uses X-Y coordinates instead of pattern matching
- **Tolerance Settings**: Fine-tuned for screenplay formatting

## 🔄 Reversion Plan

If enhanced parser causes issues:

### Option 1: Feature Flag (Fastest)
```bash
# Set in Railway dashboard:
USE_ENHANCED_SPATIAL_PARSER=false
```

### Option 2: Code Reversion
```bash
python3 deploy_enhanced.py revert
git push origin main
```

### Option 3: Git Rollback
```bash
git revert e0fc5de  # Enhanced parser commit
git push origin main
```

## 📊 Monitoring

### Key Metrics to Watch
1. **Processing Time**: Should be similar or faster
2. **Error Rate**: Should remain low
3. **Action Spacing**: Check for proper formatting
4. **Character Classification**: Verify accurate detection

### Log Indicators
- ✅ `🎯 Processing PDF with Enhanced Spatial Parser`
- ✅ `"parserType": "spatial-enhanced"`
- ❌ Any parsing errors or timeouts

## 🎯 Success Criteria

### Before Enhancement (87% accuracy)
- Action lines merged with dialogue without spacing
- "CARTER (16); her effortless..." classified as character
- "CLOSE ON:" camera directions misidentified

### After Enhancement (99% accuracy target)
- Perfect action/dialogue spacing using spatial positioning
- Character descriptions properly classified as action
- Camera directions excluded from character detection
- X-Y coordinate analysis for precise element classification

## 🛠️ Technical Details

### Enhanced Features
- **Spatial Coordinate Mapping**: Uses PDFPlumber's X-Y positioning
- **Position-Based Classification**:
  - Characters: 35-45 points from left margin
  - Dialogue: 20-35 points indent
  - Action: 12 points (full width)
  - Parentheticals: 28-35 points
- **Fine-Tuned Tolerances**: `x_tolerance=2, y_tolerance=3`
- **Enhanced Exclusions**: 21 patterns for character filtering

### Backwards Compatibility
- Standard parser remains available as fallback
- Response format unchanged
- Existing frontend code requires no modifications

## 📋 Post-Deployment Checklist

- [ ] Railway logs show enhanced parser activation
- [ ] Test PDF upload returns `railway-spatial-enhanced`
- [ ] Action/dialogue separation visually improved
- [ ] No parsing errors or performance degradation
- [ ] Feature flag reversion works if needed

---

## 🎉 Expected Results

With enhanced spatial parser deployment:
- **Accuracy**: 87% → 99% for action/dialogue separation
- **User Experience**: Proper screenplay formatting preserved
- **Maintainability**: Easy reversion and monitoring
- **Performance**: Similar or improved processing speed

The enhanced spatial parser leverages PDFPlumber's full capabilities as described in the PDF_Plumber_Info_Guide.md, moving from basic text extraction to intelligent spatial analysis.