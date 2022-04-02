package com.parkingsmart.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.parkingsmart.dto.ProvinceDTO;
import com.parkingsmart.entity.ProvinceEntity;
import com.parkingsmart.mapper.ProvinceMapper;
import com.parkingsmart.repository.ProvinceRepository;
import com.parkingsmart.service.IProvinceService;

@Service
public class ProvinceService implements IProvinceService{
	
	@Autowired
	private ProvinceRepository repository;

	@Autowired
	private ProvinceMapper mapper;
	@Override
	public List<ProvinceDTO> findAll() {
		List<ProvinceEntity> provinces = repository.findAll();
		List<ProvinceDTO> list = new ArrayList<ProvinceDTO>();
		
		for (ProvinceEntity item:provinces) {
			list.add(mapper.ToDTO(item));
		}
		return list.isEmpty()?null:list;
	}
	@Override
	public ProvinceDTO findOneById(String id) {
		Optional<ProvinceEntity> province = repository.findById(id);
		if (province.isPresent()) {
			return mapper.ToDTO(province.get());
		}
		return null;
	}

}
