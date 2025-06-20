import os
import re

def check_file_exists(file_path):
    """
    Check if a file exists and is not empty.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file exists and is not empty, False otherwise
    """
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, create it if it doesn't.
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def parse_xml_screenplay_to_dict(xml_content):
    """
    Parse XML screenplay content into a Python dictionary using regular expressions.
    
    Args:
        xml_content (str): XML content as string
        
    Returns:
        dict: Parsed screenplay as dictionary
    """
    try:
        # Clean the XML content by removing any leading text before <screenplay>
        start_tag = xml_content.find('<screenplay>')
        end_tag = xml_content.rfind('</screenplay>')
        
        if start_tag == -1 or end_tag == -1:
            raise ValueError("Could not find <screenplay> tags in the content")
        
        # Extract only the XML part
        xml_part = xml_content[start_tag:end_tag + len('</screenplay>')]
        
        # Initialize the dictionary structure
        screenplay_dict = {
            "title": "",
            "characters": [],
            "scenes": []
        }
        
        # Parse title using regex
        title_match = re.search(r'<title>(.*?)</title>', xml_part, re.DOTALL)
        if title_match:
            screenplay_dict["title"] = title_match.group(1).strip()
        
        # Parse characters using regex
        characters_match = re.search(r'<characters>(.*?)</characters>', xml_part, re.DOTALL)
        if characters_match:
            characters_content = characters_match.group(1)
            # Find all character blocks
            character_blocks = re.findall(r'<character>(.*?)</character>', characters_content, re.DOTALL)
            
            for character_block in character_blocks:
                character = {}
                
                # Extract character_number
                char_num_match = re.search(r'<character_number>(.*?)</character_number>', character_block)
                if char_num_match:
                    character["character_number"] = int(char_num_match.group(1).strip())
                
                # Extract character_name
                char_name_match = re.search(r'<character_name>(.*?)</character_name>', character_block)
                if char_name_match:
                    character["character_name"] = char_name_match.group(1).strip()
                
                # Extract character_gender
                char_gender_match = re.search(r'<character_gender>(.*?)</character_gender>', character_block)
                if char_gender_match:
                    character["character_gender"] = char_gender_match.group(1).strip()
                
                # Extract character_agegroup
                char_age_match = re.search(r'<character_agegroup>(.*?)</character_agegroup>', character_block)
                if char_age_match:
                    character["character_agegroup"] = char_age_match.group(1).strip()
                
                screenplay_dict["characters"].append(character)
        
        # Parse scenes using regex
        scenes_match = re.search(r'<scenes>(.*?)</scenes>', xml_part, re.DOTALL)
        if scenes_match:
            scenes_content = scenes_match.group(1)
            # Find all scene blocks
            scene_blocks = re.findall(r'<scene>(.*?)</scene>', scenes_content, re.DOTALL)
            
            for scene_block in scene_blocks:
                scene = {}
                
                # Extract scene_number
                scene_num_match = re.search(r'<scene_number>(.*?)</scene_number>', scene_block)
                if scene_num_match:
                    scene["scene_number"] = int(scene_num_match.group(1).strip())
                
                # Extract scene_characters
                scene_chars_match = re.search(r'<scene_characters>(.*?)</scene_characters>', scene_block, re.DOTALL)
                if scene_chars_match:
                    scene["scene_characters"] = []
                    char_nums = re.findall(r'<character_number>(.*?)</character_number>', scene_chars_match.group(1))
                    for char_num in char_nums:
                        scene["scene_characters"].append(int(char_num.strip()))
                
                # Extract scene_setting
                scene_setting_match = re.search(r'<scene_setting>(.*?)</scene_setting>', scene_block, re.DOTALL)
                if scene_setting_match:
                    scene["scene_setting"] = scene_setting_match.group(1).strip()
                
                # Extract dialogue
                dialogue_match = re.search(r'<dialogue>(.*?)</dialogue>', scene_block, re.DOTALL)
                if dialogue_match:
                    scene["dialogue"] = []
                    dialogue_content = dialogue_match.group(1)
                    # Find all dialogue_entry blocks
                    dialogue_entries = re.findall(r'<dialogue_entry>(.*?)</dialogue_entry>', dialogue_content, re.DOTALL)
                    
                    for dialogue_entry_block in dialogue_entries:
                        dialogue_entry = {}
                        
                        # Extract character_number from dialogue
                        dialog_char_match = re.search(r'<character_number>(.*?)</character_number>', dialogue_entry_block)
                        if dialog_char_match:
                            dialogue_entry["character_number"] = dialog_char_match.group(1).strip()
                        
                        # Extract dialog
                        dialog_match = re.search(r'<dialog>(.*?)</dialog>', dialogue_entry_block, re.DOTALL)
                        if dialog_match:
                            dialogue_entry["dialog"] = dialog_match.group(1).strip()
                        
                        scene["dialogue"].append(dialogue_entry)
                
                screenplay_dict["scenes"].append(scene)
        
        return screenplay_dict
        
    except Exception as e:
        print(f"Error parsing XML screenplay: {e}")
        return None

def clean_screenplay_content(content):
    """
    Clean the screenplay content by removing any extra text and repetitive instructions.
    
    Args:
        content (str): Raw screenplay content
        
    Returns:
        str: Cleaned XML content
    """
    # Find the start and end of the actual screenplay XML
    start_tag = content.find('<screenplay>')
    end_tag = content.rfind('</screenplay>')
    
    if start_tag == -1 or end_tag == -1:
        return content
    
    # Extract only the XML part
    xml_part = content[start_tag:end_tag + len('</screenplay>')]
    
    return xml_part 