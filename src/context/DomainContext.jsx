import { createContext, useContext, useState, useEffect } from 'react';

const DomainContext = createContext();

export const useDomain = () => useContext(DomainContext);

export const DomainProvider = ({ children }) => {
  const [domainConfig, setDomainConfig] = useState({
    domain: 'localhost',
    isB2B: false,
    priceKey: 'price_garba', // default
    showSliders: true,
    showWelcomeOffer: true
  });

  useEffect(() => {
    // In production, this would be window.location.hostname
    const hostname = window.location.hostname;
    // For local testing you could check a localStorage value or VITE env var
    // Hardcoded logic for now based on domain names:
    
    let isB2B = false;
    let priceKey = 'price_garba'; // def
    let showSliders = true;
    let showWelcomeOffer = true;

    if (hostname.includes('ttd.in')) {
      isB2B = true;
      priceKey = 'price_ttd';
    } else if (hostname.includes('garba.shop')) {
      isB2B = false;
      priceKey = 'price_garba';
    } else if (hostname.includes('maharashtra') || hostname.includes('maha')) {
      isB2B = true;
      priceKey = 'price_maha';
    } 
    // Fallback logic for localhost testing
    else {
      const testDomain = localStorage.getItem('test_domain') || 'garba.shop';
      if (testDomain === 'ttd.in') {
        isB2B = true;
        priceKey = 'price_ttd';
      } else if (testDomain === 'maha') {
        isB2B = true;
        priceKey = 'price_maha';
      }
    }

    if (isB2B) {
      showSliders = false;
      showWelcomeOffer = false;
    }

    setDomainConfig({
      domain: hostname,
      isB2B,
      priceKey,
      showSliders,
      showWelcomeOffer
    });
  }, []);

  return (
    <DomainContext.Provider value={domainConfig}>
      {children}
    </DomainContext.Provider>
  );
};
