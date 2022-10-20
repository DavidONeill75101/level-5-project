import React, { Component } from 'react';
import axios from "axios";

import Link from 'next/link'
import Table from 'react-bootstrap/Table'



export default class Index extends Component {
	constructor(props) {
		super(props)

        this.state = {
			loaded: false,
			collated: []
		}
		
		this.refreshCollated = this.refreshCollated.bind(this);

	}

    refreshCollated() {
        var self = this
        axios.get('http://127.0.0.1:5000/get_collated?start=0&end=10')
		.then(function (response) {
			const collated = response.data
            self.setState( {
				collated: collated,
				loaded: true
			} )		
		})
		.catch(function (error) {
			console.log(error);
		})
		.then(function () {
			// always executed
		});  
    }

    componentDidMount() {
		this.refreshCollated()
	}

	
	render() {
        
	
        var contents = 'loading'

        
        
		if (this.state.loaded) {
            
            
			const rows = this.state.collated.map(c => <tr key={c.matching_id}><td>{c.evidencetype}</td><td>{c.gene_normalized}</td><td>{c.cancer_normalized}</td><td>{c.drug_normalized}</td><td>{c.variant_group}</td><td>{c.citation_count}</td><td><Link href={"/sentences/"}><a>Review Annotations</a></Link></td></tr>)
			
			contents = <Table striped bordered hover>
				<thead>
					<tr>
						<th>Evidence Type</th>
                        <th>Gene</th>
                        <th>Cancer</th>
                        <th>Drug</th>
						<th>Variant</th>
                        <th># of Papers</th>
					</tr>
				</thead>
				<tbody>
					{rows}
				</tbody>
			</Table>
            
          
		}
		
		return (
			
			
			
            <div>
                <div className="d-sm-flex align-items-center justify-content-between mb-4 titlepadding"><h1 className="h3 mb-0 text-gray-800">CIViCMine Annotation Review</h1></div>
                <div>{contents}</div>            
            </div>

            
            
       
		)
	}
}

