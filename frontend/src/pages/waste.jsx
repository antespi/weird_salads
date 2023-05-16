import React from 'react';
import MainLayout from '../layouts/main';
import Inventory from '../components/inventory';

const Waste = () => {
  return (
    <MainLayout>
      <h1>Waste</h1>
      <Inventory source='waste' submitLabel='Waste'/>
    </MainLayout>
  );
}

export default Waste;
