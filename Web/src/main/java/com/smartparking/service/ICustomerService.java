package com.smartparking.service;

import java.util.List;

import com.smartparking.dto.CustomerDTO;
import com.smartparking.entity.CustomerEntity;

public interface ICustomerService {
	
	public void save(CustomerDTO customer);
	public List<CustomerDTO> findAll();
	public void update(String id, String customerCard);
	public List<CustomerEntity> findByCustomerCardNot(String customerCard);
	public CustomerEntity findByEmailAndPassword(String email);

}
