# Architecture Diagrams

## Overview

The `architecture-comparison.excalidraw` file contains side-by-side visual comparisons of the REST and MCP implementations.

## How to View

### Option 1: Excalidraw.com
1. Go to https://excalidraw.com
2. Click "Open" in the menu
3. Select `docs/architecture-comparison.excalidraw`
4. View and edit the diagrams

### Option 2: VS Code Extension
1. Install the "Excalidraw" extension in VS Code
2. Open `docs/architecture-comparison.excalidraw`
3. Diagrams render inline

## Diagram Contents

### REST Implementation (Left - Blue)

**Flow:**
```
User/CLI
   ↓ HTTP GET
REST Client (AlphaVantageRESTClient)
   ↓ Request
Alpha Vantage REST API (/query)
   ↑ JSON Response
```

**Characteristics:**
- ✓ Stateless
- ✓ Direct
- ✓ JSON Format

### MCP Implementation (Right - Green)

**Flow:**
```
User/CLI
   ↓ JSON-RPC POST
MCP Plugin (AlphaVantageMCPPlugin)
   ↓ initialize
MCP Server (mcp.alphavantage.co/mcp)
   ↓ TOOL_CALL → GLOBAL_QUOTE
Alpha Vantage REST API
   ↑ CSV Response
```

**Characteristics:**
- ✓ Stateful
- ✓ Protocol Layer
- ✓ CSV Format
- ✓ Plugin Interface

## Key Visual Differences

| Aspect | REST | MCP |
|--------|------|-----|
| **Layers** | 2 (Client → API) | 3 (Plugin → MCP → API) |
| **Color Coding** | Blue theme | Green theme |
| **Protocol** | Simple HTTP GET | JSON-RPC over HTTP POST |
| **Abstraction** | Direct connection | Plugin interface + Protocol |
| **Response Path** | Direct return | Through protocol layer |

## Editing the Diagrams

The `.excalidraw` file is JSON-based and can be:
- Edited visually at excalidraw.com
- Version controlled with git
- Embedded in documentation
- Exported to PNG/SVG for presentations

## File Location

```
docs/
└── architecture-comparison.excalidraw
```

This diagram complements the code examples by providing a visual understanding of the architectural differences between the two approaches.
