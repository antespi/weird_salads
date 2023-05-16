import React from 'react';
import MainLayout from '../layouts/main';
import Inventory from '../components/inventory';

const Reception = () => {

  return (
    <MainLayout>
      <h1>Reception</h1>
      <Inventory source='delivery' submitLabel='Receive' refLabel='Shipping Ref'/>
    </MainLayout>
  );
}

export default Reception;
