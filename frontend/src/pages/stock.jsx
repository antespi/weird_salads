import React from 'react';
import MainLayout from '../layouts/main';
import Inventory from '../components/inventory';

const Stock = () => {
  return (
    <MainLayout>
      <h1>Stock</h1>
      <Inventory source='stock' submitLabel='Set stock'/>
    </MainLayout>
  );
}

export default Stock;
