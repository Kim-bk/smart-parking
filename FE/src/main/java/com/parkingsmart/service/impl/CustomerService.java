package com.parkingsmart.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.parkingsmart.dto.CustomerDTO;
import com.parkingsmart.mapper.CustomerMapper;
import com.parkingsmart.repository.CustomerRepository;
import com.parkingsmart.service.ICustomerService;

@Service
public class CustomerService implements ICustomerService{
	
	@Autowired
	private CustomerRepository repository;
	
	@Autowired
	private CustomerMapper mapper;
	

	@Override
	public void save(CustomerDTO customer) {
		customer.setId("KH01");
		repository.save(mapper.toEntity(customer)); 
	}

}
