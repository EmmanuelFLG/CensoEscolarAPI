import React, { useEffect, useState } from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';

const geoUrl = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const estadosBrasileiros = [
  'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará',
  'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão',
  'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará',
  'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro',
  'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima',
  'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
];

const getColorBasedOnMatriculas = (matriculas, maxMatriculas) => {
  if (!matriculas) return '#ddd';
  const ratio = matriculas / maxMatriculas;
  if (ratio > 0.8) return '#1B5E20';
  if (ratio > 0.6) return '#2E7D32';
  if (ratio > 0.4) return '#388E3C';
  if (ratio > 0.2) return '#43A047';
  return '#81C784';
};

const Mapa = () => {
  const [matriculasData, setMatriculasData] = useState([]);
  const [selectedYear, setSelectedYear] = useState('2023');
  const [selectedState, setSelectedState] = useState('Todos');
  const [loading, setLoading] = useState(false);
  const [maxMatriculas, setMaxMatriculas] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:5000/censoescolar?ano=${selectedYear}${selectedState !== 'Todos' ? `&estado=${selectedState}` : ''}`
        );
        const data = await response.json();
        setMatriculasData(data);
        if (data.length > 0) {
          const max = Math.max(...data.map(item => item.total_matriculas || 0));
          setMaxMatriculas(max);
        } else {
          setMaxMatriculas(0);
        }
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedYear, selectedState]);

  const getMatriculasForState = (stateName) => {
    const estadoData = matriculasData.find(item => item.estado === stateName);
    return estadoData ? estadoData.total_matriculas : 0;
  };

  const getStateColor = (stateName) => {
    if (selectedState !== 'Todos' && selectedState !== stateName) {
      return '#ccc';
    }
    const matriculas = getMatriculasForState(stateName);
    return getColorBasedOnMatriculas(matriculas, maxMatriculas);
  };

  return (
    <div style={{ 
      display: 'flex', 
      height: '90vh', 
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      alignItems: 'stretch'
    }}>
      <aside
        style={{
          width: 260,
          backgroundColor: '#fff0f5',
          padding: 20,
          borderRight: '3px solid #d32f2f',
          display: 'flex',
          flexDirection: 'column',
          gap: 30,
          boxShadow: '4px 0 15px rgba(211,47,47,0.15)',
          height: '100%',
          boxSizing: 'border-box'
        }}
      >
        <h2 style={{ color: '#b71c1c', marginBottom: 10 }}>Filtros</h2>

        <div>
          <label htmlFor="year-select" style={{ fontWeight: '600', color: '#880e4f' }}>Ano</label>
          <select
            id="year-select"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            style={{
              width: '100%',
              padding: 10,
              borderRadius: 8,
              border: '1px solid #f48fb1',
              marginTop: 6,
              cursor: 'pointer',
              fontSize: 16,
              backgroundColor: '#fff',
              color: '#880e4f'
            }}
          >
            <option value="2023">2023</option>
            <option value="2024">2024</option>
          </select>
        </div>

        <div>
          <label htmlFor="state-select" style={{ fontWeight: '600', color: '#880e4f' }}>Estado</label>
          <select
            id="state-select"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            style={{
              width: '100%',
              padding: 10,
              borderRadius: 8,
              border: '1px solid #f48fb1',
              marginTop: 6,
              cursor: 'pointer',
              fontSize: 16,
              backgroundColor: '#fff',
              color: '#880e4f'
            }}
          >
            <option value="Todos">Todos os Estados</option>
            {estadosBrasileiros.map(e => (
              <option key={e} value={e}>{e}</option>
            ))}
          </select>
        </div>

        {loading && (
          <p style={{
            color: '#d32f2f',
            fontWeight: 600,
            marginTop: 20,
            textAlign: 'center'
          }}>Carregando dados...</p>
        )}
      </aside>

      <main style={{ 
        flexGrow: 1, 
        position: 'relative', 
        height: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{ scale: 700, center: [-53, -15] }}
          width={900}
          height={700}
          style={{ backgroundColor: '#fff', cursor: 'default' }}
        >
          <Geographies geography={geoUrl}>
            {({ geographies }) =>
              geographies.map(geo => {
                const estadoName = geo.properties.name;
                const matriculas = getMatriculasForState(estadoName);
                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={getStateColor(estadoName)}
                    stroke={selectedState === estadoName ? '#b71c1c' : '#d32f2f'}
                    strokeWidth={selectedState === estadoName ? 1.8 : 0.8}
                    data-tooltip-id="tooltip-mapa"
                    data-tooltip-content={`${estadoName} (${selectedYear}) - Matrículas: ${matriculas.toLocaleString('pt-BR')}`}
                    onClick={() => setSelectedState(estadoName)}
                    style={{
                      default: { outline: 'none' },
                      hover: { fill: '#f48fb1', outline: 'none', cursor: 'pointer' },
                      pressed: { outline: 'none' },
                    }}
                  />
                );
              })
            }
          </Geographies>
        </ComposableMap>

        <Tooltip id="tooltip-mapa" />
      </main>
    </div>
  );
};

export default Mapa;
