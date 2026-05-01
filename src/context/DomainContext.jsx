import { createContext, useContext, useState } from 'react';

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

// Resolve domain config synchronously — no useEffect, no async delay
const resolveConfig = () => {
  const hostname = window.location.hostname;

  if (hostname.includes('ttd.in')) {
    return { domain: hostname, ...DOMAIN_CONFIGS['ttd.in'] };
  }
  if (hostname.includes('garba.shop')) {
    return { domain: hostname, ...DOMAIN_CONFIGS['garba.shop'] };
  }
  if (hostname.includes('maharashtra') || hostname.includes('maha')) {
    return { domain: hostname, ...DOMAIN_CONFIGS['maharashtra'] };
  }

  // localhost — read from localStorage for dev testing
  const testDomain = localStorage.getItem('test_domain') || 'garba.shop';
  const matched = DOMAIN_CONFIGS[testDomain] || DOMAIN_CONFIGS['garba.shop'];
  return { domain: testDomain, ...matched };
};

export const DomainProvider = ({ children }) => {
  // useState with initializer function — runs once synchronously before first render
  const [domainConfig] = useState(resolveConfig);

  return (
    <DomainContext.Provider value={domainConfig}>
      {children}
    </DomainContext.Provider>
  );
};
