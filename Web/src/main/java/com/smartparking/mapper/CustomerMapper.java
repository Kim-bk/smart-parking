package com.smartparking.mapper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.smartparking.dto.AddressDTO;
import com.smartparking.dto.CustomerDTO;
import com.smartparking.entity.AddressEntity;
import com.smartparking.entity.CustomerEntity;
import com.smartparking.service.impl.AddressService;


@Component
public class CustomerMapper {
	
	@Autowired
	private AddressMapper addressMapper;
	
	@Autowired
	private AddressService addressService;
	
	public CustomerEntity toEntity(CustomerDTO customer) {
		CustomerEntity entity = new CustomerEntity();
		
		
		
		AddressDTO address = new AddressDTO();
		address.setIdProvince(customer.getIdProvince());
		address.setIdDistrict(customer.getIdDistrict());
		address.setIdWard(customer.getIdWard());
		address.setSpecificAddress(customer.getSpecificAddress());
		
		AddressDTO address_customer = addressService.save(address);
		entity.setAddress(addressMapper.toEntity(address_customer));
		
		entity.setEmail(customer.getEmail());
		entity.setName(customer.getName());
		entity.setNumberPhone(customer.getNumberPhone());
		entity.setId(customer.getId());
		
		return entity;
	}

}
