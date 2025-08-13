"""
Configuration settings for Blockchain Research AI Agent
"""
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

# AI Agent Configuration
USE_CUSTOM_AGENT = os.getenv("USE_CUSTOM_AGENT", "false").lower() == "true"
ANKR_API_KEY = os.getenv("ANKR_API_KEY", "")
ANKR_API_URL = "https://rpc.ankr.com/multichain"

# Application Settings
APP_TITLE = "Blockchain Research & Advisory AI Agent"
APP_DESCRIPTION = "Find the perfect blockchain protocol for your project"
VERSION = "1.0.0"

# Streamlit Configuration
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": "🔗",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Color Palette (from design spec)
COLORS = {
    "primary_blue": "#1E3A8A",
    "secondary_blue": "#3B82F6", 
    "light_blue": "#EFF6FF",
    "success_green": "#059669",
    "danger_red": "#DC2626",
    "warning_orange": "#D97706",
    "purple": "#7C3AED",
    "dark_gray": "#111827",
    "medium_gray": "#6B7280",
    "light_gray": "#F3F4F6",
    "white": "#FFFFFF"
}

# Supported Blockchain Protocols
BLOCKCHAIN_PROTOCOLS = {
    "ethereum": {
        "name": "Ethereum",
        "symbol": "ETH",
        "type": "Layer 1",
        "consensus": "Proof of Stake",
        "website": "https://ethereum.org"
    },
    "solana": {
        "name": "Solana", 
        "symbol": "SOL",
        "type": "Layer 1",
        "consensus": "Proof of History + PoS",
        "website": "https://solana.com"
    },
    "polygon": {
        "name": "Polygon",
        "symbol": "MATIC", 
        "type": "Layer 2",
        "consensus": "Proof of Stake",
        "website": "https://polygon.technology"
    },
    "binance": {
        "name": "BNB Smart Chain",
        "symbol": "BNB",
        "type": "Layer 1", 
        "consensus": "Proof of Stake Authority",
        "website": "https://www.bnbchain.org"
    },
    "avalanche": {
        "name": "Avalanche",
        "symbol": "AVAX",
        "type": "Layer 1",
        "consensus": "Avalanche Consensus",
        "website": "https://www.avax.network"
    },
    "cardano": {
        "name": "Cardano",
        "symbol": "ADA", 
        "type": "Layer 1",
        "consensus": "Ouroboros PoS",
        "website": "https://cardano.org"
    },
    "polkadot": {
        "name": "Polkadot",
        "symbol": "DOT",
        "type": "Layer 0",
        "consensus": "Nominated PoS", 
        "website": "https://polkadot.network"
    },
    "cosmos": {
        "name": "Cosmos",
        "symbol": "ATOM",
        "type": "Layer 0",
        "consensus": "Tendermint BFT",
        "website": "https://cosmos.network"
    },
    "near": {
        "name": "NEAR Protocol", 
        "symbol": "NEAR",
        "type": "Layer 1",
        "consensus": "Doomslug PoS",
        "website": "https://near.org"
    },
    "fantom": {
        "name": "Fantom",
        "symbol": "FTM",
        "type": "Layer 1", 
        "consensus": "Lachesis PoS",
        "website": "https://fantom.foundation"
    },
    "algorand": {
        "name": "Algorand",
        "symbol": "ALGO",
        "type": "Layer 1",
        "consensus": "Pure PoS",
        "website": "https://algorand.com"
    },
    "tezos": {
        "name": "Tezos", 
        "symbol": "XTZ",
        "type": "Layer 1",
        "consensus": "Liquid PoS",
        "website": "https://tezos.com"
    },
    "arbitrum": {
        "name": "Arbitrum",
        "symbol": "ARB",
        "type": "Layer 2",
        "consensus": "Optimistic Rollup",
        "website": "https://arbitrum.io"
    },
    "optimism": {
        "name": "Optimism",
        "symbol": "OP", 
        "type": "Layer 2",
        "consensus": "Optimistic Rollup",
        "website": "https://optimism.io"
    },
    "chainlink": {
        "name": "Chainlink",
        "symbol": "LINK",
        "type": "Oracle Network",
        "consensus": "Decentralized Oracle",
        "website": "https://chain.link"
    }
}

# Use Case Templates
USE_CASES = {
    "gaming": {
        "name": "Gaming & NFTs",
        "description": "High throughput, low latency, affordable transactions",
        "priorities": {"tps": 0.3, "latency": 0.25, "fees": 0.25, "security": 0.2},
        "min_requirements": {"tps": 1000, "max_fee": 0.1}
    },
    "smart_contracts": {
        "name": "Smart Contract Applications", 
        "description": "Security-first with mature tooling",
        "priorities": {"security": 0.4, "ecosystem": 0.3, "tools": 0.2, "fees": 0.1},
        "min_requirements": {"security_score": 8, "ecosystem_score": 80}
    },
    "enterprise": {
        "name": "Enterprise Solutions",
        "description": "Compliance, governance, and scalability",
        "priorities": {"governance": 0.3, "compliance": 0.25, "scalability": 0.25, "security": 0.2},
        "min_requirements": {"governance_score": 7, "compliance_rating": "B+"}
    },
    "payments": {
        "name": "Payments & Transfers",
        "description": "Fast, cheap, and reliable transactions", 
        "priorities": {"speed": 0.35, "fees": 0.35, "stability": 0.2, "adoption": 0.1},
        "min_requirements": {"finality_time": 10, "max_fee": 0.01}
    },
    "nft": {
        "name": "NFT Marketplace",
        "description": "Creator-friendly with rich ecosystem",
        "priorities": {"fees": 0.3, "ecosystem": 0.25, "tools": 0.25, "community": 0.2},
        "min_requirements": {"max_fee": 0.05, "nft_support": True}
    }
}

# Evaluation Parameters
EVALUATION_PARAMS = {
    "technical": [
        "tps", "latency", "finality_time", "block_size", 
        "smart_contracts", "programming_languages"
    ],
    "economic": [
        "transaction_fees", "gas_price", "staking_yield", 
        "inflation_rate", "market_cap", "trading_volume"
    ],
    "security": [
        "consensus_mechanism", "validator_count", "attack_resistance",
        "audit_history", "bug_bounty", "incident_history"  
    ],
    "ecosystem": [
        "dapp_count", "developer_activity", "tvl", "user_count",
        "community_size", "institutional_support"
    ],
    "governance": [
        "governance_model", "voting_mechanism", "proposal_process",
        "upgrade_mechanism", "decentralization_score"
    ]
}

# API Timeouts and Limits
API_CONFIG = {
    "timeout": 30,
    "max_retries": 3,
    "retry_delay": 1,
    "cache_ttl": 300  # 5 minutes
}