import { createContext, useContext, useState, useEffect } from 'react';

const DomainContext = createContext();

export const useDomain = () => useContext(DomainContext);

// Per-domain brand config
const DOMAIN_CONFIGS = {
  'garba.shop': {
    brandName: 'garba.shop',
    tagline: 'Premium Garba & Ethnic Wear',
    primaryColor: 'pink',
    isB2B: false,
    priceKey: 'price_b2c',
    showSliders: true,
    showWelcomeOffer: true,
    supportEmail: 'support@garba.shop',
    supportPhone: '+91 98765 43210',
  },
  'ttd.in': {
    brandName: 'TTD Fashion',
    tagline: 'Wholesale Ethnic Wear',
    primaryColor: 'indigo',
    isB2B: true,
    priceKey: 'price_b2b_ttd',
    showSliders: false,
    showWelcomeOffer: false,
    supportEmail: 'support@ttd.in',
    supportPhone: '+91 98765 43210',
  },
  'maharashtra': {
    brandName: 'MH Fashion',
    tagline: 'Maharashtra Wholesale',
    primaryColor: 'orange',
    isB2B: true,
    priceKey: 'price_b2b_maharashtra',
    showSliders: false,
    showWelcomeOffer: false,
    supportEmail: 'support@mhfashion.in',
    supportPhone: '+91 98765 43210',
  },
};

const DEFAULT_CONFIG = DOMAIN_CONFIGS['garba.shop'];

export const DomainProvider = ({ children }) => {
  const [domainConfig, setDomainConfig] = useState({
    domain: 'localhost',
    ...DEFAULT_CONFIG,
  });

  useEffect(() => {
    const hostname = window.location.hostname;

    let matched = DEFAULT_CONFIG;
    let resolvedDomain = hostname;

    if (hostname.includes('ttd.in')) {
      matched = DOMAIN_CONFIGS['ttd.in'];
    } else if (hostname.includes('garba.shop')) {
      matched = DOMAIN_CONFIGS['garba.shop'];
    } else if (hostname.includes('maharashtra') || hostname.includes('maha')) {
      matched = DOMAIN_CONFIGS['maharashtra'];
    } else {
      // localhost fallback — read from localStorage for dev testing
      const testDomain = localStorage.getItem('test_domain') || 'garba.shop';
      matched = DOMAIN_CONFIGS[testDomain] || DEFAULT_CONFIG;
      resolvedDomain = testDomain;
    }

    setDomainConfig({ domain: resolvedDomain, ...matched });
  }, []);

  return (
    <DomainContext.Provider value={domainConfig}>
      {children}
    </DomainContext.Provider>
  );
};
