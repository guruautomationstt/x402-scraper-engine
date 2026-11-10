export interface X402ScraperConfig {
  endpoint?: string;
  sessionKey?: string;
  internalKey?: string;
}

export class X402Scraper {
  private endpoint: string;
  private sessionKey?: string;
  private internalKey?: string;

  constructor(config: X402ScraperConfig = {}) {
    this.endpoint = (config.endpoint || 'https://x402-scraper-engine.gejoe-tt.workers.dev').replace(/\/$/, '');
    this.sessionKey = config.sessionKey;
    this.internalKey = config.internalKey;
  }

  private headers(receipt?: string): Record<string, string> {
    const h: Record<string, string> = {
      'User-Agent': 'x402-TS-Client/1.5',
      'Content-Type': 'application/json'
    };
    if (this.sessionKey) h['X-Session-Key'] = this.sessionKey;
    if (this.internalKey) h['X-ASOT-Internal-Key'] = this.internalKey;
    if (receipt) h['X-Payment-Receipt'] = receipt;
    return h;
  }

  /**
   * Instant 1-tap proxy read returning clean Markdown
   */
  async read(url: string, receipt?: string): Promise<string> {
    const cleanUrl = url.startsWith('http') ? url : `https://${url}`;
    const res = await fetch(`${this.endpoint}/read/${cleanUrl}`, {
      headers: this.headers(receipt)
    });
    if (!res.ok && res.status !== 402) {
      throw new Error(`Scrape failed with status ${res.status}: ${await res.text()}`);
    }
    return res.text();
  }

  /**
   * Scrape webpage and return structured Markdown payload ($0.005 USDC)
   */
  async scrape(url: string, receipt?: string): Promise<any> {
    const res = await fetch(`${this.endpoint}/v1/scrape`, {
      method: 'POST',
      headers: this.headers(receipt),
      body: JSON.stringify({ url })
    });
    return res.json();
  }

  /**
   * Extract structured JSON adhering strictly to a schema via Edge Llama-3 ($0.030 USDC)
   */
  async extract(url: string, schema?: Record<string, any>, prompt?: string, receipt?: string): Promise<any> {
    const res = await fetch(`${this.endpoint}/v1/extract`, {
      method: 'POST',
      headers: this.headers(receipt),
      body: JSON.stringify({ url, schema, prompt })
    });
    return res.json();
  }
}
