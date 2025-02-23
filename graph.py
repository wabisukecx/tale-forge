"""
シーン関係図機能を提供するモジュール
"""
import graphviz
import streamlit as st

def show_graph_tab():
    """シーン関係図タブの表示"""
    try:
        graph = graphviz.Digraph()
        graph.attr(rankdir='LR')
        
        for _, row in st.session_state.data.iterrows():
            scene_id = str(row['ID']).strip()
            if not scene_id or scene_id.lower() == 'none':
                continue
                
            story = str(row['ストーリー']).strip()
            if not story or story.lower() == 'none':
                story = "..."
            story_preview = story[:20] + "..." if len(story) > 20 else story
            graph.node(scene_id, f"{scene_id}\n{story_preview}")
            
            for i in range(1, 4):
                choice = str(row[f'選択{i}']).strip()
                dest = str(row[f'選択{i}遷移先']).strip()
                
                if (choice and dest and 
                    choice.lower() != 'none' and 
                    dest.lower() != 'none'):
                    choice_preview = choice[:15] + "..." if len(choice) > 15 else choice
                    graph.edge(scene_id, dest, choice_preview)
        
        st.graphviz_chart(graph)
        
    except Exception as e:
        st.error(f"シーン関係図の生成に失敗しました: {str(e)}")