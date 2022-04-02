package com.parkingsmart.mapper;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.parkingsmart.dto.AddressDTO;
import com.parkingsmart.dto.CustomerDTO;
import com.parkingsmart.entity.CustomerEntity;
import com.parkingsmart.service.impl.AddressService;

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
