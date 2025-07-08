# Tale Forge - Interactive Gamebook Scenario Editor

Tale Forge is a comprehensive web-based application for creating, editing, and playing interactive fiction gamebooks. Built with Streamlit, it provides a complete toolkit for authors who want to create branching narrative experiences with character management, dice mechanics, and visual storytelling elements.

## What is Tale Forge?

Tale Forge bridges the gap between traditional gamebook creation tools and modern interactive fiction platforms. Think of it as a digital workshop where you can craft Choose Your Own Adventure-style stories with the depth and mechanics of tabletop role-playing games.

The application serves two primary audiences: **creators** who want to design interactive narratives, and **players** who want to experience those stories with full character management and dice-rolling mechanics.

## Core Features

### 1. Scene-Based Story Editor
The heart of Tale Forge is its intuitive scene editor, which treats your story as a collection of interconnected scenes. Each scene contains:
- **Story Text**: The narrative content that players will read
- **Multiple Choice Options**: Up to three branching paths from each scene
- **Destination Mapping**: Clear connections showing where each choice leads
- **Image Support**: Visual elements including SVG graphics for enhanced storytelling

### 2. Visual Story Flow Mapping
Understanding complex branching narratives can be challenging. Tale Forge automatically generates interactive flowcharts that show:
- How scenes connect to each other
- The flow of player choices through your story
- Dead ends and circular paths in your narrative
- Missing or undefined scene connections

### 3. Complete Character Management System
Players get a full character sheet experience with:
- **Core Attributes**: Skill, Stamina, and Luck values with initial and current tracking
- **Dice Rolling**: Built-in 2d6 mechanics for combat and luck tests
- **Optional Fear System**: Configurable psychological stress mechanics
- **Notes System**: Integrated inventory and hint tracking

### 4. TOML-Based Data Format
Your scenarios are saved in human-readable TOML format, making them:
- Easy to version control with Git
- Simple to edit in external text editors
- Portable between different installations
- Readable for collaboration with other authors

## Installation and Setup

### Prerequisites
Tale Forge requires Python 3.11 or higher and can run locally or in cloud environments like GitHub Codespaces.

### Local Installation
```bash
# Clone or download the project files
# Install required dependencies
pip install streamlit pandas graphviz toml

# Run the application
streamlit run app.py
```

### Development Container Setup
The project includes a complete development container configuration for GitHub Codespaces or local Docker development:

```json
{
  "name": "Python 3",
  "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bullseye",
  "updateContentCommand": "pip3 install --user streamlit pandas graphviz toml",
  "postAttachCommand": {
    "server": "streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false"
  }
}
```

## Application Architecture

Tale Forge is built with a modular architecture that separates concerns cleanly:

### Core Modules

**app.py** - Main application controller that:
- Initializes the Streamlit interface with three primary tabs
- Manages session state for scenario data and images
- Handles automatic loading of default scenarios
- Coordinates between editing, visualization, and gameplay modes

**editor.py** - Scene editing functionality that:
- Provides an interactive data grid for editing scenes
- Manages image uploads and associations with scenes
- Handles TOML import/export operations
- Automatically saves changes to maintain data persistence

**graph.py** - Visual relationship mapping that:
- Generates Graphviz diagrams showing scene connections
- Processes choice text and destinations into readable flowcharts
- Handles undefined scene references gracefully
- Provides interactive tooltips for detailed information

**gameplay.py** - Player experience coordinator that:
- Integrates character management with story progression
- Manages the game state during play sessions
- Coordinates dice rolling with narrative events
- Provides seamless transitions between story scenes

### Supporting Systems

**character_sheet.py** - Complete character management including:
- Procedural stat generation using dice mechanics
- Real-time stat modification with proper bounds checking
- Integrated dice rolling for combat and luck tests
- Flexible notes system for inventory and clues

**story_viewer.py** - Interactive story presentation featuring:
- Dynamic image display with SVG support and responsive scaling
- Choice presentation with clear navigation
- Scene transition management
- Error handling for missing or corrupted data

**toml_export.py** - Data serialization system that:
- Converts pandas DataFrames to structured TOML format
- Handles image path references and file management
- Provides robust error handling for malformed data
- Maintains compatibility with external editing tools

## Understanding the Data Structure

Tale Forge organizes your gamebook using a straightforward but powerful data model. Each scene in your story becomes a row in a structured table with these key components:

### Scene Identification
Every scene needs a unique identifier (ID) that serves as its address in your story. This could be simple numbers (1, 2, 3) or descriptive names (Forest_Entrance, Dragon_Lair, Victory).

### Story Content
The main narrative text that players will read when they reach this scene. This supports basic formatting and can be as short as a single sentence or as long as several paragraphs.

### Choice Architecture
Each scene can have up to three choices, and each choice requires two pieces of information:
- The choice text that players will see (like "Enter the dark forest")
- The destination scene ID where that choice leads (like "Forest_Entrance")

### Image Integration
Scenes can have associated images stored in the `images/` directory. The system supports common formats like PNG and JPEG, plus SVG graphics for scalable illustrations.

## Creating Your First Gamebook

Let's walk through creating a simple gamebook to understand how Tale Forge works in practice.

### Step 1: Design Your Story Structure
Before you start writing, sketch out your story flow on paper. Think about:
- What's your opening scene?
- What are the major decision points?
- How do different paths through your story create different experiences?
- Where do story branches converge or diverge?

### Step 2: Create Your Opening Scene
Start with a scene ID like "Start" and write engaging opening text that immediately presents the player with an interesting choice. For example:

**Scene ID**: Start
**Story**: "You stand at the edge of a mysterious forest. Ancient trees tower above you, their branches creaking in the wind. A narrow path disappears into the shadows ahead, while to your right, you notice smoke rising from what might be a cottage chimney."

**Choice 1**: "Follow the forest path" → Forest_Path
**Choice 2**: "Investigate the cottage" → Cottage
**Choice 3**: "Turn back to town" → Town_Return

### Step 3: Build Connected Scenes
Create the scenes that your choices reference. Each new scene should advance the story and present new choices that feel meaningful and consequential.

### Step 4: Add Visual Elements
Upload images that enhance your story's atmosphere. The system automatically associates images with scenes based on matching filenames, so an image named "Forest_Path.jpg" will appear when players reach the Forest_Path scene.

### Step 5: Test Your Story Flow
Use the graph visualization to see how your scenes connect. Look for:
- Dead ends that might need additional choices
- Circular references that could trap players
- Missing scene connections that need to be created

## Character Mechanics Integration

Tale Forge includes a complete character system inspired by classic gamebook mechanics. Understanding how to integrate these systems into your story creates more engaging player experiences.

### Attribute System
The three core attributes serve different narrative purposes:
- **Skill**: Represents combat ability and general competence
- **Stamina**: Health points that decrease from injuries or exhaustion
- **Luck**: A finite resource for getting out of difficult situations

### Dice Integration
The built-in dice system supports several common gamebook mechanics:
- **Combat Resolution**: Players roll 2d6 and add their Skill value
- **Luck Tests**: Roll 2d6 against current Luck value
- **Random Events**: Single d6 rolls for various story outcomes

### Fear System (Optional)
When enabled in settings.toml, the Fear system adds psychological pressure:
- Fear increases as players encounter disturbing or dangerous situations
- High Fear values can limit player options or force specific choices
- Players must balance courage against caution in their decisions

## Advanced Features

### SVG Graphics Support
Tale Forge includes sophisticated SVG handling that:
- Automatically scales vector graphics to fit display areas
- Preserves image quality at any size
- Supports complex illustrations with embedded styling
- Maintains proper aspect ratios across different devices

### Responsive Image Display
The image system adapts to different screen sizes and layouts:
- Automatically chooses between single-column and two-column layouts
- Scales images appropriately while maintaining readability
- Handles missing or corrupted image files gracefully

### Session State Management
The application maintains complete game state including:
- Current character statistics and modifications
- Player's current location in the story
- Notes and inventory items collected
- Image associations and display preferences

## Configuration Options

### settings.toml
The settings file controls optional features:
```toml
show_fear = true  # Enable/disable the Fear attribute system
```

### Image Directory Structure
Images are stored in a dedicated directory with automatic organization:
```
images/
├── Scene1.png
├── Forest_Path.svg
├── Dragon_Lair.jpg
└── Victory.png
```

## Data Format Specification

Tale Forge uses TOML (Tom's Obvious, Minimal Language) for data storage because it strikes an ideal balance between human readability and machine parsing. Here's how your scenario data is structured:

### Scene Definition Format
```toml
[Scene_ID]
story = "Your narrative text here"
choices = ["First choice", "Second choice", "Third choice"]
destinations = ["Scene_A", "Scene_B", "Scene_C"]
image = "images/Scene_ID.png"  # Optional
```

### Complete Example
```toml
[Start]
story = "You awaken in a dimly lit dungeon cell. The heavy wooden door stands slightly ajar, and you can hear distant footsteps echoing down the corridor outside."
choices = ["Sneak out quietly", "Call for help", "Search the cell"]
destinations = ["Corridor", "Guard_Encounter", "Hidden_Item"]
image = "images/Start.png"

[Corridor]
story = "The corridor stretches in both directions, lit by flickering torches. You can see stairs leading up to your left, and the passage continues into darkness to your right."
choices = ["Take the stairs up", "Continue into the darkness", "Return to your cell"]
destinations = ["Upper_Level", "Deep_Dungeon", "Start"]
```

## Troubleshooting Common Issues

### Scene Connection Problems
If the graph view shows disconnected or missing scenes, check that:
- Scene IDs in destinations exactly match the actual scene IDs
- There are no extra spaces or special characters in IDs
- All referenced scenes actually exist in your data

### Image Display Issues
When images don't appear correctly:
- Verify the image file exists in the images/ directory
- Check that file extensions match the references in your data
- Ensure SVG files have proper viewBox attributes for scaling

### Character System Problems
If dice rolling or character stats behave unexpectedly:
- Confirm that initial character generation completed successfully
- Check that stat modifications stay within valid ranges
- Verify that the Fear system setting matches your story's needs

## Extending Tale Forge

The modular architecture makes Tale Forge easily extensible for custom needs:

### Adding New Character Attributes
Modify `character_sheet.py` to include additional stats like Wisdom, Charisma, or Magic Points. The system automatically handles display and modification mechanics.

### Custom Dice Mechanics
Extend the dice rolling system in `character_sheet.py` to support different die types (d4, d8, d10) or complex roll formulas.

### Enhanced Image Support
The image handling system in `story_viewer.py` can be extended to support additional formats or provide image editing capabilities.

### Alternative Data Formats
While TOML is the default, the export system in `toml_export.py` can be adapted to support JSON, YAML, or other structured data formats.

## Best Practices for Gamebook Creation

### Narrative Structure
- Start with compelling opening choices that immediately engage players
- Ensure every scene advances the story or reveals character information
- Create meaningful consequences for player decisions
- Plan multiple paths to the same outcomes to accommodate different play styles

### Character Integration
- Use attribute tests sparingly but meaningfully
- Allow multiple approaches to overcome challenges
- Provide ways for players to recover from setbacks
- Balance random chance with player skill and planning

### Technical Considerations
- Keep scene IDs short but descriptive
- Test your story flow regularly using the graph view
- Backup your scenario files frequently
- Use version control for collaborative projects

Tale Forge represents a powerful platform for interactive storytelling that combines the accessibility of modern web applications with the depth and complexity that makes gamebooks engaging. Whether you're crafting a simple adventure or a complex narrative with multiple storylines, Tale Forge provides the tools you need to bring your interactive fiction to life.
