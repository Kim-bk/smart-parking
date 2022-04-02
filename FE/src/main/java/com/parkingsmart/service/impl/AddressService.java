package com.parkingsmart.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.parkingsmart.dto.AddressDTO;
import com.parkingsmart.entity.AddressEntity;
import com.parkingsmart.mapper.AddressMapper;
import com.parkingsmart.repository.AddressRepository;
import com.parkingsmart.service.IAddressService;

@Service
public class AddressService implements IAddressService{

	@Autowired
	private AddressRepository repository;
	
	@Autowired
	private AddressMapper mapper;

	@Override
	public AddressDTO save(AddressDTO address) {
		AddressEntity addressEntity = mapper.toEntity(address);
		AddressEntity addSave = repository.save(addressEntity);
		return mapper.toDTO(addSave);
	}
	
	
}
