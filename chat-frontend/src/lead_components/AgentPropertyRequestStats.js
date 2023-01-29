
import React, { PureComponent } from 'react';
import {
  PieChart, Pie, Sector,Cell,} from 'recharts';
import styled from 'styled-components';
import { Statistic } from 'semantic-ui-react';


const StatsWrapper = styled.div`
    width:100%;
    height: 100%;
    border-radius:10px;
    background-color:#fff;
    padding: 0 10px;
    overflow-y:auto;
    -webkit-box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
    box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
`

const ContentHeader = styled.h4`
height: 35px;
position: sticky;
background-color: #fff;
border-radius: 20px;
z-index: 5;
top: 0px;
display: flex;
justify-content: center;
align-items: center;
-webkit-box-shadow: 0 1px 3px 0 #63f1eb24, 0 0 0 1px #63f1eb24;
box-shadow: 0 1px 3px 0 #63f1eb24, 0 0 0 1px #63f1eb24;
`

const ContentHeaderTwo = styled.h5`
  background-color: #fff;
  text-align:left;
  @media (max-width: 786px){
  text-align:center;
  }
`

const StatsBoard = styled.div`
  width:100%;
  height: 20%;
  border-radius:10px;
  background-color:#fff;
  padding: 0 10px;
  overflow-y:auto;
  -webkit-box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  box-shadow: 0 1px 3px 0 #fff, 0 0 0 1px #fff;
  display:flex;
  flex-direction:column;
  justify-content:center;
`
const CustomPieChart = styled(PieChart)`
  display:flex;
  justify-content:center;
  align-items:center;
  @media (max-width: 786px){
    width:100% !important;
  }
`

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042',
'#FF0000','#0000FF','#FFFF00','#FFA500','#800080','#FF00FF','#800000'];

const renderActiveShape = (props) => {
  const RADIAN = Math.PI / 180;
  const {
    cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle,
    fill, payload, percent, value,
  } = props;

  return (
    <g>
      <text x={cx} y={cy-12} dy={20} textAnchor="middle" fill={fill}>{payload.name}</text>
      <text x={cx} y={cy-12} dy={8} textAnchor="middle" fill={fill}>{payload.value}</text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 2}
        outerRadius={outerRadius + 5}
        fill={fill}
      />
    </g>
  );
};


export default class AgentPropertyRequestStats extends PureComponent {
  state = {
    activeIndex:0,
    _activeIndex:0,
  };

  onPieEnter = (data, index) => {
    this.setState({
      activeIndex:index,
    });
  };
  _onPieEnter = (data, index) => {
    this.setState({
      _activeIndex:index,
    });
  };
  render() {
    const totalRequests= this.props.leads.length;
    var buyersArray =  this.props.leads.filter(function(request) {
        return request.ownership === "BUY";
    });
    var rentersArray =  this.props.leads.filter(function(request) {
        return request.ownership === "RENT";
    });
    var lesseesArray =  this.props.leads.filter(function(request) {
        return request.ownership === "LEASE";
    });

    var apartmentsArray =  this.props.leads.filter(function(request) {
        return request.property_type === "APARTMENT";
    });
    var bungalowsArray =  this.props.leads.filter(function(request) {
        return request.property_type === "BUNGALOW";
    });
    var condosArray =  this.props.leads.filter(function(request) {
        return request.property_type === "CONDOMINIUM";
    });
    var dormsArray =  this.props.leads.filter(function(request) {
        return request.property_type === "DORMITORY";
    });
    var duplexArray =  this.props.leads.filter(function(request) {
        return request.property_type === "DUPLEX";
    });
    var mansionsArray =  this.props.leads.filter(function(request) {
        return request.property_type === "MANSION";
    });
    var singleFamilyArray =  this.props.leads.filter(function(request) {
        return request.property_type === "SINGLEFAMILY";
    });
    var terracedArray =  this.props.leads.filter(function(request) {
        return request.property_type === "TERRACED";
    });
    var townhouseArray =  this.props.leads.filter(function(request) {
        return request.property_type === "TOWNHOUSE";
    });
    var landArray =  this.props.leads.filter(function(request) {
        return request.property_type === "LAND";
    });
    var otherTypesArray =  this.props.leads.filter(function(request) {
        return request.property_type === "OTHER";
    });

    const data = [
      { name: 'Buyers', value: buyersArray.length, color:'#0088FE'},
      { name: 'Renters', value: rentersArray.length, color:'#00C49F'},
      { name: 'Lessees', value: lesseesArray.length, color:'#FFBB28'},
    ];
    const propertyTypeData = [
      {
        name: 'Apartment', value: apartmentsArray.length,in:"ap",color:'#0088FE',
      },
      {
        name: 'Bungalow', value: bungalowsArray.length,in:"bu",color:'#00C49F',
      },
      {
        name: 'Condominium', value: condosArray.length,in:"co",color:'#FFBB28',
      },
      {
        name: 'Dormitory', value: dormsArray.length,in:"do",color:'#FF8042',
      },
      {
        name: 'Duplex', value: duplexArray.length,in:"du",color:'#FF0000',
      },
      {
        name: 'Mansion', value: mansionsArray.length,in:"ma",color:'#0000FF',
      },
      {
        name: 'Single-family', value: singleFamilyArray.length,in:"si",color:'#FFFF00',
      },
      {
        name: 'Terraced house', value: terracedArray.length,in:"te",color:'#FFA500',
      },
      {
        name: 'Townhouse', value: townhouseArray.length,in:"to",color:'#800080',
      },
      {
        name: 'Land', value: landArray.length,in:"la",color:'#FF00FF',
      },
      {
        name: 'Other', value: otherTypesArray.length,in:"ot",color:'#800000',
      },
    ];
    var dataValueArray =  data.filter(function(request) {
        return request.value > 0;
    });
    var propTypeDataValueArray =  propertyTypeData.filter(function(request) {
        return request.value > 0;
    });
    return (
          <StatsWrapper>
              <ContentHeader>STATISTICS</ContentHeader>
              <StatsBoard>
                  <Statistic color='purple'>
                    <Statistic.Value>{totalRequests}</Statistic.Value>
                    <Statistic.Label>Total Requests</Statistic.Label>
                  </Statistic>
              </StatsBoard>
              <ContentHeaderTwo>Request Types</ContentHeaderTwo>
              {dataValueArray.length > 0 ? (
                  <CustomPieChart width={200} height={150}>
                    <Pie
                      activeIndex={this.state._activeIndex}
                      activeShape={renderActiveShape}
                      data={data}
                      cx={100}
                      cy={70}
                      innerRadius={50}
                      outerRadius={60}
                      fill="#8884d8"
                      dataKey="value"
                      onMouseEnter={this._onPieEnter}
                    >
                      {
                        data.map((entry, index) =><Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
                      }
                    </Pie>
                  </CustomPieChart>
              ) : (
                <StatsBoard>
                    <Statistic color='blue'>
                      <Statistic.Value>0</Statistic.Value>
                      <Statistic.Label>Results</Statistic.Label>
                    </Statistic>
                </StatsBoard>
              )
              }
              <ContentHeaderTwo>Property Types</ContentHeaderTwo>
              { propTypeDataValueArray.length > 0 ? (
                  <CustomPieChart width={200} height={230}>
                    <Pie
                      activeIndex={this.state.activeIndex}
                      activeShape={renderActiveShape}
                      data={propertyTypeData}
                      cx={100}
                      cy={90}
                      innerRadius={50}
                      outerRadius={60}
                      paddingAngle={5}
                      fill="#8884d8"
                      dataKey= "value"
                      onMouseEnter={this.onPieEnter}
                    >
                      {
                        propertyTypeData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
                      }
                    </Pie>
                  </CustomPieChart>
                ) : (
                  <StatsBoard>
                      <Statistic color='blue'>
                        <Statistic.Value>0</Statistic.Value>
                        <Statistic.Label>Results</Statistic.Label>
                      </Statistic>
                  </StatsBoard>
                )
              }
      </StatsWrapper>
    );
  }
}
