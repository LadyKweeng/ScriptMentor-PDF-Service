from typing import Dict, List, Any

class QualityCalculator:
    """Calculate parsing quality metrics based on screenplay structure"""
    
    def calculate_quality(self, pdf, pages_data: List[Dict], scenes: List[str], 
                         characters: set, dialogue_blocks: List[str], 
                         action_blocks: List[str]) -> Dict[str, Any]:
        """Calculate comprehensive quality metrics"""
        
        total_pages = len(pdf.pages)
        total_lines = sum(len(page['lines']) for page in pages_data)
        total_words = sum(page['word_count'] for page in pages_data)
        
        # Scene detection quality (target: 90%+)
        scene_density = len(scenes) / total_pages if total_pages > 0 else 0
        scene_quality = min(1.0, scene_density / 1.5)  # ~1.5 scenes per page average
        
        # Character detection quality (target: 70%+)
        char_count = len(characters)
        char_density = char_count / total_pages if total_pages > 0 else 0
        char_quality = min(1.0, char_density / 0.5)  # ~0.5 chars per page average
        
        # Dialogue/Action balance (target: 94%+)
        dialogue_count = len(dialogue_blocks)
        action_count = len(action_blocks)
        total_content = dialogue_count + action_count
        
        if total_content > 0:
            dialogue_ratio = dialogue_count / total_content
            # Good screenplays typically have 40-60% dialogue
            balance_quality = 1.0 - abs(dialogue_ratio - 0.5) * 2
        else:
            balance_quality = 0.0
        
        # Page preservation (target: 79%+)
        page_quality = min(1.0, total_words / (total_pages * 250)) if total_pages > 0 else 0
        
        # Overall score (weighted average)
        overall_score = (
            scene_quality * 0.35 +      # Scene detection most important
            balance_quality * 0.30 +    # Dialogue/action balance critical
            page_quality * 0.20 +       # Page accuracy important
            char_quality * 0.15         # Character detection (being improved)
        )
        
        return {
            'overallScore': round(overall_score, 3),
            'sceneDetection': round(scene_quality, 3),
            'characterDetection': round(char_quality, 3),
            'dialogueActionBalance': round(balance_quality, 3),
            'pagePreservation': round(page_quality, 3),
            'metrics': {
                'totalPages': total_pages,
                'totalScenes': len(scenes),
                'totalCharacters': char_count,
                'totalDialogueBlocks': dialogue_count,
                'totalActionBlocks': action_count,
                'totalWords': total_words
            }
        }