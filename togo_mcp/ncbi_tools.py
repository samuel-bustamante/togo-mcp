"""
NCBI E-utilities search tools for TogoMCP.

Provides keyword search functionality for NCBI databases using the esearch API:
- NCBI Gene (ncbigene)
- NCBI Taxonomy (taxonomy)
- ClinVar (clinvar)
- MedGen (medgen)
- PubMed (pubmed)
- PubChem Compound (pccompound)
- PubChem Substance (pcsubstance)
- PubChem BioAssay (pcassay)

Requires NCBI_API_KEY environment variable for optimal rate limits (10 req/sec vs 3 req/sec).
"""

import os
import asyncio
import httpx
from typing import Optional, List, Dict, Any
from mcp.types import TextContent
from .server import toolcall_log
from fastmcp import FastMCP


# Get API key from environment
NCBI_API_KEY = os.environ.get("NCBI_API_KEY")
NCBI_EMAIL = os.environ.get("NCBI_EMAIL", "your-email@example.com")  # NCBI recommends providing email

# Rate limiting
RATE_LIMIT_DELAY = 0.1 if NCBI_API_KEY else 0.34  # 10/sec with key, 3/sec without

ncbi_mcp = FastMCP("NCBI API server")

class NCBISearchError(Exception):
    """Custom exception for NCBI API errors"""
    pass


# Database configuration with metadata
NCBI_DATABASES = {
    "gene": {
        "label": "NCBI Gene",
        "id_label": "Gene IDs",
        "url_template": "https://www.ncbi.nlm.nih.gov/gene/{id}",
        "description": "Search for genes by name, symbol, or other identifiers",
        "example_query": "BRCA1 AND human[organism]",
        "supported_fields": ["organism", "gene"],
    },
    "taxonomy": {
        "label": "NCBI Taxonomy",
        "id_label": "Taxonomy IDs (TaxIDs)",
        "url_template": "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={id}",
        "description": "Search for organisms and taxonomic information",
        "example_query": "Escherichia coli",
        "supported_fields": ["scientific name", "common name"],
    },
    "clinvar": {
        "label": "ClinVar",
        "id_label": "Variation IDs",
        "url_template": "https://www.ncbi.nlm.nih.gov/clinvar/variation/{id}",
        "description": "Search for genetic variants and clinical interpretations",
        "example_query": "BRCA1 AND pathogenic",
        "supported_fields": ["gene", "condition"],
    },
    "medgen": {
        "label": "MedGen",
        "id_label": "Concept IDs (CUIs)",
        "url_template": "https://www.ncbi.nlm.nih.gov/medgen/{id}",
        "description": "Search for medical genetics concepts and conditions",
        "example_query": "breast cancer",
        "supported_fields": ["concept", "condition"],
    },
    "pubmed": {
        "label": "PubMed",
        "id_label": "PubMed IDs (PMIDs)",
        "url_template": "https://pubmed.ncbi.nlm.nih.gov/{id}",
        "description": "Search biomedical literature",
        "example_query": "CRISPR gene editing",
        "supported_fields": ["title", "author", "journal"],
    },
    "pccompound": {
        "label": "PubChem Compound",
        "id_label": "Compound IDs (CIDs)",
        "url_template": "https://pubchem.ncbi.nlm.nih.gov/compound/{id}",
        "description": "Search for unique chemical structures",
        "example_query": "aspirin",
        "supported_fields": ["name", "formula", "molecular weight"],
    },
    "pcsubstance": {
        "label": "PubChem Substance",
        "id_label": "Substance IDs (SIDs)",
        "url_template": "https://pubchem.ncbi.nlm.nih.gov/substance/{id}",
        "description": "Search for depositor-provided chemical records",
        "example_query": "caffeine",
        "supported_fields": ["name", "source"],
    },
    "pcassay": {
        "label": "PubChem BioAssay",
        "id_label": "Assay IDs (AIDs)",
        "url_template": "https://pubchem.ncbi.nlm.nih.gov/assay/assay.cgi?aid={id}",
        "description": "Search for biological screening data",
        "example_query": "kinase inhibitor",
        "supported_fields": ["target", "assay type"],
    },
}


async def _ncbi_esearch_api(
    db: str,
    term: str,
    retmax: int = 20,
    retstart: int = 0,
    sort: Optional[str] = None,
    field: Optional[str] = None
) -> Dict[str, Any]:
    """
    Core function to query NCBI E-utilities esearch API.
    
    Args:
        db: NCBI database name
        term: Search query
        retmax: Maximum number of results
        retstart: Starting index for pagination
        sort: Sort order (database-specific)
        field: Specific field to search in
    
    Returns:
        Parsed JSON response from NCBI
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        "db": db,
        "term": term,
        "retmax": retmax,
        "retstart": retstart,
        "retmode": "json",
        "tool": "TogoMCP",
        "email": NCBI_EMAIL
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    
    if sort:
        params["sort"] = sort
    
    if field:
        params["field"] = field
    
    # Rate limiting
    await asyncio.sleep(RATE_LIMIT_DELAY)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check for errors in NCBI response
            if "error" in data:
                raise NCBISearchError(f"NCBI API error: {data['error']}")
            
            return data
            
        except httpx.HTTPError as e:
            raise NCBISearchError(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            raise NCBISearchError(f"Error querying NCBI: {str(e)}")


def _format_esearch_result(data: Dict[str, Any], db: str, query: str) -> str:
    """Format esearch results for display"""
    esearch_result = data.get("esearchresult", {})
    
    count = esearch_result.get("count", "0")
    ids = esearch_result.get("idlist", [])
    retmax = esearch_result.get("retmax", "0")
    retstart = esearch_result.get("retstart", "0")
    query_translation = esearch_result.get("querytranslation", "N/A")
    
    # Get database metadata
    db_info = NCBI_DATABASES.get(db, {})
    db_label = db_info.get("label", db.upper())
    id_label = db_info.get("id_label", "IDs")
    url_template = db_info.get("url_template")
    
    result = f"""{db_label} Search Results
=====================================
Query: {query}
Query Translation: {query_translation}

Total Results: {count}
Returned: {len(ids)} (showing {retstart}-{int(retstart) + len(ids)})

{id_label}: {', '.join(ids)}
"""
    
    if esearch_result.get("warninglist"):
        result += f"\nWarnings: {esearch_result['warninglist']}"
    
    # Add helpful link for first result
    if url_template and ids:
        first_url = url_template.format(id=ids[0])
        result += f"\n\nView first result: {first_url}"
    
    return result


@ncbi_mcp.tool()
async def ncbi_esearch(
    database: str,
    query: str,
    max_results: int = 20,
    start_index: int = 0,
    sort_by: Optional[str] = None,
    search_field: Optional[str] = None
) -> List[TextContent]:
    """
    Search NCBI databases using E-utilities esearch API.
    
    Supports multiple NCBI databases including Gene, Taxonomy, ClinVar, MedGen,
    PubMed, and PubChem (Compound, Substance, BioAssay).
    
    Args:
        database: NCBI database name. Supported values:
            - "gene" or "ncbigene": NCBI Gene database
            - "taxonomy": NCBI Taxonomy (organism information)
            - "clinvar": ClinVar (genetic variants)
            - "medgen": MedGen (medical genetics concepts)
            - "pubmed": PubMed (biomedical literature)
            - "pccompound": PubChem Compound
            - "pcsubstance": PubChem Substance
            - "pcassay": PubChem BioAssay
        query: Search query (supports Entrez/PubMed syntax with field tags and boolean operators)
        max_results: Maximum number of results to return (default: 20)
        start_index: Starting index for pagination (default: 0)
        sort_by: Optional sort order (e.g., "relevance", "pub_date" for PubMed)
        search_field: Optional specific field to search in
    
    Returns:
        Formatted search results with database-specific IDs
    
    Examples:
        - Search for human BRCA1 gene: database="gene", query="BRCA1 AND human[organism]"
        - Search PubMed: database="pubmed", query="CRISPR gene editing"
        - Search for E. coli: database="taxonomy", query="Escherichia coli"
        - Search PubChem: database="pccompound", query="aspirin"
    """
    toolcall_log("ncbi_esearch")
    
    # Normalize database name (handle aliases)
    db_aliases = {
        "ncbigene": "gene",
    }
    normalized_db = db_aliases.get(database.lower(), database.lower())
    
    # Validate database
    if normalized_db not in NCBI_DATABASES:
        supported_dbs = ", ".join(NCBI_DATABASES.keys())
        return [TextContent(
            type="text",
            text=f"Error: Unsupported database '{database}'. Supported databases: {supported_dbs}"
        )]
    
    try:
        data = await _ncbi_esearch_api(
            db=normalized_db,
            term=query,
            retmax=max_results,
            retstart=start_index,
            sort=sort_by,
            field=search_field
        )
        result = _format_esearch_result(data, normalized_db, query)
        
        return [TextContent(type="text", text=result)]
    
    except NCBISearchError as e:
        return [TextContent(type="text", text=f"Error searching NCBI {database}: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


@ncbi_mcp.tool()
async def ncbi_list_databases() -> List[TextContent]:
    """
    List all supported NCBI databases with descriptions and example queries.
    
    Returns:
        Formatted list of available databases
    """
    toolcall_log("ncbi_list_databases")
    
    result = "Supported NCBI Databases\n" + "=" * 50 + "\n\n"
    
    for db_name, db_info in NCBI_DATABASES.items():
        result += f"{db_info['label']} (database=\"{db_name}\")\n"
        result += f"  Description: {db_info['description']}\n"
        result += f"  ID Type: {db_info['id_label']}\n"
        result += f"  Example Query: {db_info['example_query']}\n"
        result += f"  Supported Fields: {', '.join(db_info['supported_fields'])}\n\n"
    
    result += "\nUsage:\n"
    result += "  Use ncbi_esearch(database=\"<db_name>\", query=\"<your_query>\")\n"
    result += "  Example: ncbi_esearch(database=\"gene\", query=\"BRCA1 AND human[organism]\")\n"
    
    return [TextContent(type="text", text=result)]


# Additional utility functions for future use
@ncbi_mcp.tool()
async def ncbi_esummary(database: str, ids: List[str]) -> List[TextContent]:
    """
    Fetch summary information for given IDs using esummary.
    Useful for getting detailed info after esearch.
    
    Args:
        database: NCBI database name
        ids: List of IDs to fetch summaries for
    
    Returns:
        Parsed JSON response with summary data
    """
    toolcall_log("ncbi_esummary")
    
    # Normalize database name
    db_aliases = {"ncbigene": "gene"}
    normalized_db = db_aliases.get(database.lower(), database.lower())
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
    params = {
        "db": normalized_db,
        "id": ",".join(ids),
        "retmode": "json",
        "tool": "TogoMCP",
        "email": NCBI_EMAIL
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    
    await asyncio.sleep(RATE_LIMIT_DELAY)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Format the response nicely
            import json
            formatted_json = json.dumps(data, indent=2)
            return [TextContent(type="text", text=formatted_json)]
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error fetching summaries: {str(e)}")]


@ncbi_mcp.tool()
async def ncbi_efetch(
    database: str,
    ids: List[str],
    rettype: str = "xml",
    retmode: str = "text"
) -> List[TextContent]:
    """
    Fetch full records using efetch.
    Returns actual data (sequences, records, etc.)
    
    Args:
        database: NCBI database name
        ids: List of IDs to fetch
        rettype: Return type (xml, fasta, gb, etc.)
        retmode: Return mode (text, xml, json where applicable)
    
    Returns:
        Response text in requested format
    """
    toolcall_log("ncbi_efetch")
    
    # Normalize database name
    db_aliases = {"ncbigene": "gene"}
    normalized_db = db_aliases.get(database.lower(), database.lower())
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    params = {
        "db": normalized_db,
        "id": ",".join(ids),
        "rettype": rettype,
        "retmode": retmode,
        "tool": "TogoMCP",
        "email": NCBI_EMAIL
    }
    
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    
    await asyncio.sleep(RATE_LIMIT_DELAY)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            return [TextContent(type="text", text=response.text)]
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error fetching records: {str(e)}")]
