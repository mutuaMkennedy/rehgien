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


export default class ProRequestStats extends PureComponent {
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

    var qualifiedArray =  this.props.leads.filter(function(request) {
        return request.qualified === true;
    });
    var notQualifiedArray =  this.props.leads.filter(function(request) {
        return request.qualified === false;
    });
    var agentsArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "AGENT";
    });
    var propertyManagerArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "PROPERTYMANAGER";
    });
    var interiorDesignerArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "INTERIORDESIGNER";
    });
    var architectArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "ARCHITECT";
    });
    var landscapeArchitectsArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "LANDSCAPEARCHITECT";
    });
    var homeMoverArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "HOMEMOVER";
    });
    var plumbingArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "PLUMBING";
    });
    var photographerArray =  this.props.leads.filter(function(request) {
        return request.type_of_proffesional === "PHOTOGRAPHER";
    });

    const data = [
      { name: 'Qualified', value: qualifiedArray.length, color:'#0088FE'},
      { name: 'Not Qualifed', value: notQualifiedArray.length, color:'#00C49F'},
    ];
    const proTypeData = [
      {
        name: 'Agent', value: agentsArray.length,in:"ag",color:'#0088FE',
      },
      {
        name: 'P Manager', value: propertyManagerArray.length,in:"pm",color:'#00C49F',
      },
      {
        name: 'Int Designer', value: interiorDesignerArray.length,in:"id",color:'#FFBB28',
      },
      {
        name: 'Architect', value: architectArray.length,in:"ar",color:'#FF8042',
      },
      {
        name: 'Landscape arch', value: landscapeArchitectsArray.length,in:"la",color:'#FF0000',
      },
      {
        name: 'Home mover', value: homeMoverArray.length,in:"hm",color:'#0000FF',
      },
      {
        name: 'Plumbing', value: plumbingArray.length,in:"pl",color:'#FFFF00',
      },
      {
        name: 'Photographer', value: photographerArray.length,in:"ph",color:'#FFA500',
      },
    ];
    var dataValueArray =  data.filter(function(request) {
        return request.value > 0;
    });
    var proTypeDataValueArray =  proTypeData.filter(function(request) {
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
              <ContentHeaderTwo>Qualified</ContentHeaderTwo>
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
              <ContentHeaderTwo>Pro Types</ContentHeaderTwo>
              { proTypeDataValueArray.length > 0 ? (
                  <CustomPieChart width={200} height={230}>
                    <Pie
                      activeIndex={this.state.activeIndex}
                      activeShape={renderActiveShape}
                      data={proTypeData}
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
                        proTypeData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
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
